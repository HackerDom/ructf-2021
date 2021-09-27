package workerpool

import (
	"context"
	"fmt"
	"github.com/usernamedt/container-service-gin/models"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"strconv"
	"sync"
	"sync/atomic"
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
	workersCount int
	jobsCount    uint64
	jobs         chan Job
	results      chan Result
	Done         chan struct{}
}

func New(wcount int) *WorkerPool {
	return &WorkerPool{
		workersCount: wcount,
		jobs:         make(chan Job, wcount),
		results:      make(chan Result, wcount),
		Done:         make(chan struct{}),
	}
}

func (wp *WorkerPool) Run(ctx context.Context) {
	var wg sync.WaitGroup

	for i := 0; i < wp.workersCount; i++ {
		wg.Add(1)
		// fan out worker goroutines
		//reading from jobs channel and
		//pushing calcs into results channel
		go worker(ctx, &wg, wp.jobs, wp.results)
	}

	wg.Wait()
	close(wp.Done)
	close(wp.results)
}

func (wp *WorkerPool) Results() <-chan Result {
	return wp.results
}

func (wp *WorkerPool) AddJob(job Job) string {
	jobsCount := atomic.AddUint64(&wp.jobsCount, 1)
	job.Descriptor.ID = strconv.FormatUint(jobsCount, 10)
	wp.jobs <- job
	//close(wp.jobs)
	return job.Descriptor.ID
}

func Setup() {
	Pool = New(setting.AppSetting.WorkersCount)
	go Pool.Run(context.Background())

	go func() {
		for {
			select {
			case r, ok := <-Pool.Results():
				if !ok {
					continue
				}

				status := models.Success
				if r.Err != nil {
					logging.Error(fmt.Errorf("%s job error: %v", r.Descriptor.ID, r.Err))
					status = models.Error
				}

				job := models.Job{
					ID: r.Descriptor.ID,
					Status: status,
					Result: r.Value,
				}

				err := job.Update()
				if err != nil {
					logging.Error(fmt.Errorf("failed to update the job %s: %v", r.Descriptor.ID, err))
					continue
				}

			case <-Pool.Done:
				return
			default:
			}
		}
	}()
}
