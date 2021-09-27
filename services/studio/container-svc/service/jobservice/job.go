package jobservice

import (
	"context"
	"github.com/usernamedt/container-service-gin/models"
	"github.com/usernamedt/container-service-gin/pkg/executer"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
	"io"
)


type JobService struct {}


func (js *JobService) Add(binary io.Reader, ctx context.Context) (*models.Job, error) {
	id := workerpool.Pool.AddJob(workerpool.Job{
		Descriptor: workerpool.JobDescriptor{
			Metadata: binary,
		},
		ExecFn: func(ctx context.Context, payload io.Reader) ([]byte, error) {
			executer.Run(ctx, payload)
			return nil, nil
		},
	})

	job, err := models.NewJob(id)
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
