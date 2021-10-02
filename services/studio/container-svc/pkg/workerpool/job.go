package workerpool

import (
	"context"
	"io"
	"time"
)

type ExecutionFn func(ctx context.Context, payload JobDescriptor) (ExecResult, error)

type ExecResult struct {
	TimeInfo JobTimeInfo
	Res      []byte
}

type JobTimeInfo struct {
	AllocMemStart  time.Time
	AllocMemFinish time.Time
	StartContainer time.Time
	StopContainer  time.Time
	ReadMem        time.Time
	DeallocMem     time.Time
}

type JobDescriptor struct {
	ID            string
	MemID         string
	Metadata      io.Reader
	TimeInfo      JobTimeInfo
	RunCredential string
}

type Result struct {
	ExecResult ExecResult
	Err        error
	Descriptor JobDescriptor
}

type Job struct {
	Descriptor JobDescriptor
	ExecFn     ExecutionFn
}

func (j Job) execute(ctx context.Context) Result {
	value, err := j.ExecFn(ctx, j.Descriptor)
	if err != nil {
		return Result{
			Err:        err,
			Descriptor: j.Descriptor,
		}
	}

	return Result{
		ExecResult: value,
		Descriptor: j.Descriptor,
	}
}
