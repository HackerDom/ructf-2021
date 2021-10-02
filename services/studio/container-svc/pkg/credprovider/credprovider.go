package credprovider

import (
	"fmt"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/pkg/setting"
	"sync/atomic"
)

var CredentialProvider *CredProvider

func Setup() {
	var err error
	CredentialProvider, err = NewCredProvider()
	if err != nil {
		logging.Fatal(err)
	}
}

type CredProvider struct {
	pool []string
	i    uint64
}

func NewCredProvider() (*CredProvider, error) {
	credPool := setting.AppSetting.CredPoolList
	if len(credPool) == 0 {
		return nil, fmt.Errorf("empty credentials pool")
	}

	credProvider := &CredProvider{
		pool: credPool,
		i: 0,
	}
	return credProvider, nil
}

func (cp *CredProvider) Next() string {
	credIdx := atomic.AddUint64(&cp.i, 1)
	return cp.pool[credIdx % uint64(len(cp.pool))]
}
