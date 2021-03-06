package workerpool

import (
	"context"
	"fmt"
	"github.com/usernamedt/container-service-gin/models"
	"github.com/usernamedt/container-service-gin/pkg/containerkiller"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"strconv"
	"sync"
	"sync/atomic"
	"time"
)

var Pool *WorkerPool

func worker(ctx context.Context, wg *sync.WaitGroup, jobs <-chan Job, results chan<- Result) {
	defer wg.Done()
	for {
		select {
		case job, ok := <-jobs:
			if !ok {
				return
			}
			results <- job.execute(ctx)
		case <-ctx.Done():
			fmt.Printf("cancelled worker. Error detail: %v\n", ctx.Err())
			results <- Result{
				Err: ctx.Err(),
			}
			return
		}
	}
}

type WorkerPool struct {
	workersCount       int
	receivedJobsCount  uint64
	processedJobsCount uint64
	jobs               chan Job
	results            chan Result
	workerDone         chan struct{}
	queueStatDone      chan struct{}
	rpmStatDone        chan struct{}
	killerDone         chan struct{}
}

func New(wcount int) *WorkerPool {
	return &WorkerPool{
		workersCount:  wcount,
		jobs:          make(chan Job, wcount),
		results:       make(chan Result, wcount),
		workerDone:    make(chan struct{}),
		queueStatDone: make(chan struct{}),
		rpmStatDone:   make(chan struct{}),
		killerDone:    make(chan struct{}),
	}
}

func (wp *WorkerPool) Run(ctx context.Context) {
	var wg sync.WaitGroup

	wp.initQueueStatWriter()
	wp.initRpmStatWriter()
	wp.initContainerKiller()
	for i := 0; i < wp.workersCount; i++ {
		wg.Add(1)
		// fan out worker goroutines
		//reading from jobs channel and
		//pushing calcs into results channel
		go worker(ctx, &wg, wp.jobs, wp.results)
	}

	wg.Wait()
	close(wp.workerDone)
	close(wp.queueStatDone)
	close(wp.rpmStatDone)
	close(wp.killerDone)
	close(wp.results)
}

func (wp *WorkerPool) NextResult() (Result, bool, bool) {
	select {
	case r, ok := <-Pool.results:
		atomic.AddUint64(&wp.processedJobsCount, 1)
		return r, ok, false

	case <-Pool.workerDone:
		return Result{}, false, true
	}
}

func (wp *WorkerPool) GenerateJobId() string {
	id := time.Now().UnixNano()
	return strconv.FormatInt(id, 10)
}

func (wp *WorkerPool) AddJob(job Job) {
	atomic.AddUint64(&wp.receivedJobsCount, 1)
	wp.jobs <- job
}

func (wp *WorkerPool) initQueueStatWriter() {
	statInterval := setting.AppSetting.QueueStatInterval
	if statInterval == 0 {
		logging.Infof("WorkerPool: not enabling queue statistics writer")
		return
	}

	logging.Infof("WorkerPool: init queue statistics writer (each %d seconds)", statInterval)
	timer := time.NewTicker(statInterval * time.Second)
	go func() {
		for {
			select {
			case <-timer.C:
				queueSize := wp.receivedJobsCount - wp.processedJobsCount
				if queueSize == 0 {
					continue
				}
				logging.Infof("WorkerPool: queue size is %d, ", queueSize)
			case <-wp.queueStatDone:
				logging.Info("WorkerPool: stopping queue statistics writer")
				timer.Stop()
				return
			}
		}
	}()
}

func (wp *WorkerPool) initRpmStatWriter() {
	statInterval := setting.AppSetting.RequestStatInterval
	if statInterval == 0 {
		logging.Infof("WorkerPool: not enabling request statistics writer")
		return
	}

	logging.Infof("WorkerPool: init request statistics writer (each %d seconds)", statInterval)
	timer := time.NewTicker(statInterval * time.Second)
	prevProcessed := uint64(0)
	prevReceived := uint64(0)
	go func() {
		for {
			select {
			case <-timer.C:
				currProcessed := wp.processedJobsCount
				currReceived := wp.receivedJobsCount
				logging.Infof("WorkerPool: processed %d jobs, received %d jobs / %d seconds",
					currProcessed-prevProcessed, currReceived-prevReceived, statInterval)
				prevProcessed = currProcessed
				prevReceived = currReceived
			case <-wp.rpmStatDone:
				logging.Info("WorkerPool: stopping request statistics writer")
				timer.Stop()
				return
			}
		}
	}()
}

func (wp *WorkerPool) initContainerKiller() {
	period := setting.AppSetting.ContainerKillPeriod
	if period == 0 {
		logging.Fatal("WorkerPool: container killer period should be > 0")
		return
	}

	maxExecTime := int(setting.AppSetting.ContainerMaxExecTime.Seconds())
	if maxExecTime == 0 || maxExecTime >= 10 {
		logging.Fatal("WorkerPool: container killer max exec time should be in range [1,9]")
		return
	}

	logging.Infof("WorkerPool: init container killer (each %d seconds)", int(period.Seconds()))
	timer := time.NewTicker(period)
	excludedPeriods := ""
	for i := range makeRange(0, maxExecTime) {
		excludedPeriods += strconv.Itoa(i)
	}
	go func() {
		for {
			select {
			case <-timer.C:
				containerkiller.KillStuckContainers(excludedPeriods)
			case <-wp.killerDone:
				logging.Info("WorkerPool: stopping container killer")
				timer.Stop()
				return
			}
		}
	}()
}

func makeRange(min, max int) []int {
	a := make([]int, max-min+1)
	for i := range a {
		a[i] = min + i
	}
	return a
}

func Setup() {
	Pool = New(setting.AppSetting.WorkersCount)
	go Pool.Run(context.Background())

	go func() {
		for {
			r, ok, finished := Pool.NextResult()
			if finished {
				logging.Info("Worker pool has finished working")
				return
			}

			if !ok {
				continue
			}

			status := models.Success
			if r.Err != nil {
				logging.Error(fmt.Errorf("%s job error: %v", r.Descriptor.ID, r.Err))
				status = models.Error
			}

			job := models.Job{
				ID:     r.Descriptor.ID,
				MemID:  r.Descriptor.MemID,
				Status: status,
				Result: string(r.ExecResult.Res),
				TimeInfo: models.JobExecStat{
					AllocMemStart:  r.ExecResult.TimeInfo.AllocMemStart,
					StartContainer: r.ExecResult.TimeInfo.StartContainer,
					StopContainer:  r.ExecResult.TimeInfo.StopContainer,
					ReadMem:        r.ExecResult.TimeInfo.ReadMem,
					DeallocMem:     r.ExecResult.TimeInfo.DeallocMem,
				},
			}

			err := job.Update()
			if err != nil {
				logging.Error(fmt.Errorf("failed to update the job %s: %v", r.Descriptor.ID, err))
			}
		}
	}()
}
