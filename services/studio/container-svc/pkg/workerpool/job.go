package workerpool

import (
"context"
	"io"
)

type ExecutionFn func(ctx context.Context, payload JobDescriptor) ([]byte, error)

type JobDescriptor struct {
	ID       string
	MemID 	 string
	Metadata io.Reader
}

type Result struct {
	Value      []byte
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
		Value:      value,
		Descriptor: j.Descriptor,
	}
}
