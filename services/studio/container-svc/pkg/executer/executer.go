package executer

import (
	"bytes"
	"context"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"github.com/usernamedt/container-service-gin/pkg/workerpool"
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

	id := runContainer(ctx, cli, payload.MemID)

	waitContainer(ctx, cli, id)
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

func runContainer(ctx context.Context, cli *client.Client, memID string) string {
	resp, err := cli.ContainerCreate(ctx, &container.Config{
		Image: "ubuntu",
		Cmd: []string{"/bin/bash", "-c", "echo " + memID},
		Tty: false,
	}, &container.HostConfig{
		Binds:           nil,
		ContainerIDFile: "",
		LogConfig:       container.LogConfig{},
		NetworkMode:     "",
		PortBindings:    nil,
		RestartPolicy:   container.RestartPolicy{},
		AutoRemove:      false,
		//AutoRemove:      true,
		VolumeDriver:    "",
		VolumesFrom:     nil,
		CapAdd:          nil,
		CapDrop:         nil,
		CgroupnsMode:    "",
		DNS:             nil,
		DNSOptions:      nil,
		DNSSearch:       nil,
		ExtraHosts:      nil,
		GroupAdd:        nil,
		IpcMode:         "host",
		Cgroup:          "",
		Links:           nil,
		OomScoreAdj:     0,
		PidMode:         "",
		Privileged:      false,
		PublishAllPorts: false,
		ReadonlyRootfs:  false,
		SecurityOpt:     nil,
		StorageOpt:      nil,
		Tmpfs:           nil,
		UTSMode:         "",
		UsernsMode:      "",
		ShmSize:         0,
		Sysctls:         nil,
		Runtime:         "",
		ConsoleSize:     [2]uint{},
		Isolation:       "",
		Resources:       container.Resources{},
		Mounts:          nil,
		MaskedPaths:     nil,
		ReadonlyPaths:   nil,
		Init:            nil,
	}, nil, nil, "")
	if err != nil {
		panic(err)
	}

	if err := cli.ContainerStart(ctx, resp.ID, types.ContainerStartOptions{}); err != nil {
		panic(err)
	}
	return resp.ID
}

func AllocMemory(jobId string) (string, error) {
	args := []string{jobId}

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

