package containerkiller

import (
	"bytes"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"os/exec"
	"fmt"
)

func KillStuckContainers(excludedPeriods string) {
	command := fmt.Sprintf("/usr/bin/docker ps --format '{{.RunningFor}} {{.Names}}' | grep -v '[%s] seconds ago' | awk '{print $NF}' | xargs -r docker rm -f", excludedPeriods)
	args := []string{"-c", command}
	cmd := exec.Command("bash", args...)
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
	res := outputBuf.String()
	if len(res) > 0 {
		logging.Infof("stuck container killer out: %s", outputBuf.String())
	}
}


