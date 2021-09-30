package executor

import (
	"bytes"
	"context"
	"fmt"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
	"io"
	"os/exec"
	"strings"
)

func Run(ctx context.Context, payload workerpool.JobDescriptor) ([]byte, error) {
	v, err := runContainer(payload.MemID, payload.Metadata)
	if err != nil {
		errMsg := fmt.Sprintf("Executor: failed to run the container: %s, %v", v, err)
		logging.Error(errMsg)
		return []byte(errMsg), nil
	}

	res, err := readResult(payload.ID)
	if err != nil {
		errMsg := fmt.Sprintf("Executor: failed to read the container job result: %s, %v", v, err)
		logging.Error(errMsg)
		return []byte(errMsg), nil
	}
	return []byte(res), nil
}

func runContainer(memId string, payload io.Reader) (string, error) {
	launchArgs := fmt.Sprintf("cat > payload && chmod +x payload && ./payload %s", memId)
	args := []string{"run", "--ipc", "host", "-i", "ubuntu", "bash", "-c", launchArgs}

	cmd := exec.Command("docker", args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf
	cmd.Stdin = payload
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

func AllocMemory(jobId string) (string, error) {
	args := []string{jobId, setting.AppSetting.KeyPath}

	cmd := exec.Command(setting.AppSetting.AllocatorPath, args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	err := cmd.Start()
	if err != nil {
		return "", err
	}
	err = cmd.Wait()
	if err != nil {
		return "", err
	}

	return outputBuf.String(), nil
}


func DeallocMemory(jobId string) {
	args := []string{jobId, setting.AppSetting.KeyPath}

	cmd := exec.Command(setting.AppSetting.DeallocatorPath, args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
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
	err := cmd.Start()
	if err != nil {
		return "", err
	}

	err = cmd.Wait()
	if err != nil {
		return "", err
	}

	return outputBuf.String(), nil
}

