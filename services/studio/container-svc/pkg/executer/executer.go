package executer

import (
	"bytes"
	"context"
	"fmt"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
	"io"
	"os"
	"os/exec"
	"strings"
)

func Run(ctx context.Context, payload workerpool.JobDescriptor) {
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}

	_, err = cli.ImagePull(ctx, "docker.io/library/ubuntu", types.ImagePullOptions{})
	if err != nil {
		panic(err)
	}
	//io.Copy(os.Stdout, reader)

	v, err := runContainer(payload.MemID, payload.Metadata)
	if err != nil {
		logging.Error(err)
	}
	logging.Info(v)
}

func waitContainer(ctx context.Context, cli *client.Client, id string) {
	statusCh, errCh := cli.ContainerWait(ctx, id, container.WaitConditionNotRunning)
	select {
	case err := <-errCh:
		if err != nil {
			panic(err)
		}
	case <-statusCh:
	}

	out, err := cli.ContainerLogs(ctx, id, types.ContainerLogsOptions{ShowStdout: true})
	if err != nil {
		panic(err)
	}
	stdcopy.StdCopy(os.Stdout, os.Stderr, out)
}

func runContainer(memId string, payload io.Reader) (string, error) {
	launchArgs := fmt.Sprintf("cat > kek && chmod +x kek && ./kek %s", memId)
	args := []string{"run", "-i", "ubuntu",
		"bash", "-c",
		launchArgs}
	logging.Info("GOIN' to EXEC: %s", launchArgs)
	cmd := exec.Command("docker", args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stdin = payload
	cmd.Stderr = outputBuf
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

func GetMemory(out string) (string, error) {
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

