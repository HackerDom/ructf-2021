package executer

import (
	"context"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
	"io"
	"os"
)

func Run(ctx context.Context, payload io.Reader) {
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}

	reader, err := cli.ImagePull(ctx, "docker.io/library/ubuntu", types.ImagePullOptions{})
	if err != nil {
		panic(err)
	}
	io.Copy(os.Stdout, reader)

	id := runShit(ctx, cli)

	waitShit(ctx, cli, id)
}

func waitShit(ctx context.Context, cli *client.Client, id string) {
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

func runShit(ctx context.Context, cli *client.Client) string {
	resp, err := cli.ContainerCreate(ctx, &container.Config{
		Image: "ubuntu",
		//Cmd:   []string{"sleep", "3600"},
		Cmd: []string{"/bin/bash", "-c", "echo ZBS"},
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
		CapAdd:          []string{"SYS_PTRACE"},
		CapDrop:         nil,
		CgroupnsMode:    "",
		DNS:             nil,
		DNSOptions:      nil,
		DNSSearch:       nil,
		ExtraHosts:      nil,
		GroupAdd:        nil,
		IpcMode:         "",
		Cgroup:          "",
		Links:           nil,
		OomScoreAdj:     0,
		PidMode:         "host",
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
