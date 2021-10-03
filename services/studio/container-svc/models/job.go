package models

import (
	"encoding/json"
	"fmt"
	"github.com/usernamedt/container-service-gin/pkg/e"
	"github.com/usernamedt/container-service-gin/pkg/gredis"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"time"
)

type NonExistJobError struct {
	error
}

func NewNonExistJobError(id string) NonExistJobError {
	return NonExistJobError{fmt.Errorf("non-existing job id: %s", id)}
}

type JobStatus string

const (
	Created JobStatus = "created"
	Success JobStatus = "success"
	Error   JobStatus = "error"
)

type JobExecStat struct {
	AllocMemStart  time.Time
	StartContainer time.Time
	StopContainer  time.Time
	ReadMem        time.Time
	DeallocMem     time.Time
}

type Job struct {
	ID       string      `json:"run_id"`
	MemID    string      `json:"id"`
	Status   JobStatus   `json:"status"`
	Result   string      `json:"result"`
	TimeInfo JobExecStat `json:"time_info"`
}

func NewJob(id string, memId string) (*Job, error) {
	job := &Job{
		ID:     id,
		MemID:  memId,
		Status: Created,
	}
	err := gredis.Set(e.PREFIX_JOB+memId, job, getJobLifetime())
	if err != nil {
		return nil, err
	}
	return job, nil
}

func (j *Job) Update() error {
	return gredis.Set(e.PREFIX_JOB+j.MemID, j, getJobLifetime())
}

func GetJob(memId string) (*Job, error) {
	job := &Job{}
	key := e.PREFIX_JOB + memId
	if gredis.Exists(key) {
		data, err := gredis.Get(key)
		if err != nil {
			logging.Info(err)
			return nil, err
		}

		err = json.Unmarshal(data, job)
		if err != nil {
			logging.Info(err)
			return nil, err
		}

		return job, nil
	}

	return nil, NewNonExistJobError(memId)
}

func getJobLifetime() int {
	return int(setting.AppSetting.JobLifetimeMinutes.Seconds())
}
