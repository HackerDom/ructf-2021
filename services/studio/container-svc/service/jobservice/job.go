package jobservice

import (
	"context"
	"github.com/usernamedt/container-service-gin/models"
	"github.com/usernamedt/container-service-gin/pkg/executor"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
	"io"
)


type JobService struct {}


func (js *JobService) Add(binary io.Reader, ctx context.Context) (*models.Job, error) {
	jobId := workerpool.Pool.GenerateJobId()

	memId, err := executor.AllocMemory(jobId)
	if err != nil {
		return nil, err
	}

	workerpool.Pool.AddJob(workerpool.Job{
		Descriptor: workerpool.JobDescriptor{
			Metadata: binary,
			MemID: memId,
			ID: jobId,
		},
		ExecFn: func(ctx context.Context, payload workerpool.JobDescriptor) ([]byte, error) {
			defer executor.DeallocMemory(payload.ID)
			return executor.Run(ctx, payload)
		},
	})

	job, err := models.NewJob(jobId, memId)
	if err != nil {
		logging.Info(err)
		return nil, err
	}

	// add job to the pool
	return job, nil
}

func (js *JobService) Get(id string, context context.Context) (*models.Job, error) {
	job, err := models.GetJob(id)
	if err != nil {
		return nil, err
	}
	return job, nil
}
