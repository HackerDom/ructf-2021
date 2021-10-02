package jobservice

import (
	"context"
	"github.com/usernamedt/container-service-gin/models"
	"github.com/usernamedt/container-service-gin/pkg/credprovider"
	"github.com/usernamedt/container-service-gin/pkg/executor"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
	"io"
)

type JobService struct{}

func (js *JobService) Add(binary io.Reader, ctx context.Context) (*models.Job, error) {
	timeInfo := workerpool.JobTimeInfo{}
	jobId := workerpool.Pool.GenerateJobId()

	cred := credprovider.CredentialProvider.Next()

	memId, err := executor.GetJobKey(jobId, cred)

	if err != nil {
		logging.Error(err)
		return nil, err
	}

	workerpool.Pool.AddJob(workerpool.Job{
		Descriptor: workerpool.JobDescriptor{
			Metadata:      binary,
			MemID:         memId,
			ID:            jobId,
			TimeInfo:      timeInfo,
			RunCredential: cred,
		},
		ExecFn: func(ctx context.Context, payload workerpool.JobDescriptor) (workerpool.ExecResult, error) {
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
