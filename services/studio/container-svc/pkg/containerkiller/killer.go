package containerkiller

import (
	"bytes"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"os/exec"
)

func KillStuckContainers() {
	args := []string{"ps", "--format", "'{{.RunningFor}} {{.Names}}'", "|", "grep -v '[012] seconds ago'", "|",  "awk", "'{print $NF}'", "|", "xargs",  "docker rm -f"}
	cmd := exec.Command("docker", args...)
	outputBuf := bytes.NewBuffer(nil)
	cmd.Stdout = outputBuf
	cmd.Stderr = outputBuf

	err := cmd.Start()
	if err != nil {
		logging.Errorf("failed to kill stuck containers: err %v, out: %s", err, outputBuf.String())
	}
	err = cmd.Wait()
	if err != nil {
		logging.Errorf("failed to kill stuck containers: err %v, out: %s", err, outputBuf.String())
	}

	logging.Infof("stuck container killer out: %s", outputBuf.String())
}
