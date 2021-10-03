package executor

import (
	"bytes"
	"context"
	"fmt"
	"github.com/google/uuid"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
	"io"
	"os/exec"
	"strings"
	"time"
)

func Run(ctx context.Context, payload workerpool.JobDescriptor) (workerpool.ExecResult, error) {
	timeInfo := payload.TimeInfo
	defer DeallocMemory(payload.ID)
	v, err := AllocMemory(payload.ID, payload.RunCredential)
	if err != nil {
		errMsg := fmt.Sprintf("Executor: failed to allocate memory: %s, %v; job_id %s, mem_id %s, runcred %s", v, err, payload.ID, payload.MemID, payload.RunCredential)
		logging.Error(errMsg)
		return workerpool.ExecResult{Res: []byte(errMsg), TimeInfo: timeInfo}, nil
	}

	timeInfo.StartContainer = time.Now()
	v, err = runContainer(payload.MemID, payload.Metadata, payload.RunCredential)
	timeInfo.StopContainer = time.Now()

	if err != nil {
		errMsg := fmt.Sprintf("Executor: failed to run the container: %s, %v; job_id %s, mem_id %s, runcred %s", v, err, payload.ID, payload.MemID, payload.RunCredential)
		logging.Error(errMsg)
		return workerpool.ExecResult{Res: []byte(errMsg), TimeInfo: timeInfo}, nil
	}

	timeInfo.ReadMem = time.Now()
	res, err := readResult(payload.ID)
	if err != nil {
		errMsg := fmt.Sprintf("Executor: failed to read the container job result: %s, %v; job_id %s, mem_id %s, runcred %s", res, err, payload.ID, payload.MemID, payload.RunCredential)
		logging.Error(errMsg)
		return workerpool.ExecResult{Res: []byte(errMsg), TimeInfo: timeInfo}, nil
	}

	timeInfo.DeallocMem = time.Now()
	return workerpool.ExecResult{Res: []byte(res), TimeInfo: timeInfo}, nil
}

func runContainer(memId string, payload io.Reader, username string) (string, error) {
	launchArgs := fmt.Sprintf("cat > ~/payload && chmod +x ~/payload && ~/payload %s", memId)
	containerId := uuid.NewString()
	args := []string{"run", "--rm", "--network", "none", "--cpus", ".05", "--memory", "25M", "--name", containerId, "--user", username, "--ipc", "host", "-i", "basealpine", "timeout", "1", "ash", "-c", launchArgs}

	cmd := exec.Command("docker", args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf
	cmd.Stdin = payload
	err := cmd.Start()
	if err != nil {
		return outputBuf.String(), err
	}

	done := make(chan error)
	go func() { done <- cmd.Wait() }()
	select {
	case err = <-done:
		if err != nil {
			return outputBuf.String(), err
		}
	case <-time.After(180 * time.Second):
		return "container killed (timeout)", terminateContainer(containerId)
	}

	return outputBuf.String(), nil
}

func AllocMemory(jobId string, cred string) (string, error) {
	arg := fmt.Sprintf("%s %s %s", setting.AppSetting.AllocatorPath, jobId, setting.AppSetting.KeyPath)

	cmd := exec.Command("su", "-", cred, "-c", arg)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf

	err := cmd.Start()
	if err != nil {
		return "", fmt.Errorf("failed to allocate memory: err %v, out: %s", err, outputBuf.String())
	}
	err = cmd.Wait()
	if err != nil {
		return "", fmt.Errorf("failed to allocate memory: err %v, out: %s", err, outputBuf.String())
	}

	return outputBuf.String(), nil
}

func GetJobKey(jobId string, cred string) (string, error) {
	arg := fmt.Sprintf("%s %s %s", setting.AppSetting.KeyGenPath, jobId, setting.AppSetting.KeyPath)

	cmd := exec.Command("su", "-", cred, "-c", arg)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf

	err := cmd.Start()
	if err != nil {
		return "", fmt.Errorf("failed to generate key: err %v, out: %s", err, outputBuf.String())
	}
	err = cmd.Wait()
	if err != nil {
		return "", fmt.Errorf("failed togenerate key: err %v, out: %s", err, outputBuf.String())
	}

	return outputBuf.String(), nil
}

func DeallocMemory(jobId string) {
	args := []string{jobId, setting.AppSetting.KeyPath}

	cmd := exec.Command(setting.AppSetting.DeallocatorPath, args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf

	err := cmd.Start()
	if err != nil {
		logging.Errorf("Error during dealloc: %v", err)
	}
	err = cmd.Wait()
	if err != nil {
		logging.Errorf("Error during dealloc: %v", err)
	}
}

func readResult(out string) (string, error) {
	args := strings.Split(out, " ")
	args = append(args, setting.AppSetting.KeyPath)
	cmd := exec.Command(setting.AppSetting.ReaderPath, args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf
	err := cmd.Start()
	if err != nil {
		return outputBuf.String(), err
	}

	err = cmd.Wait()
	if err != nil {
		return outputBuf.String(), err
	}

	return outputBuf.String(), nil
}

func terminateContainer(id string) error {
	cmd := exec.Command("docker", "rm", "--force", id)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf

	err := cmd.Start()
	if err != nil {
		return fmt.Errorf("failed to kill container: err %v, out: %s", err, outputBuf.String())
	}
	err = cmd.Wait()
	if err != nil {
		return fmt.Errorf("failed to kill container: err %v, out: %s", err, outputBuf.String())
	}

	return fmt.Errorf("container killed (timeout)")
}
