package v1

import (
	"bytes"
	"github.com/astaxie/beego/validation"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
	"github.com/usernamedt/container-service-gin/models"
	"github.com/usernamedt/container-service-gin/pkg/app"
	"github.com/usernamedt/container-service-gin/pkg/e"
	"github.com/usernamedt/container-service-gin/pkg/logging"
	"github.com/usernamedt/container-service-gin/service/jobservice"
	"io"
	"net/http"
)

// @Router /api/v1/jobs/{id} [get]
func GetJob(c *gin.Context) {
	appG := app.Gin{C: c}
	id := com.StrTo(c.Param("id")).String()
	valid := validation.Validation{}
	valid.AlphaNumeric(id, "id")

	if valid.HasErrors() {
		app.MarkErrors(valid.Errors)
		appG.Response(http.StatusBadRequest, e.INVALID_PARAMS, nil)
		return
	}

	jobService := jobservice.JobService{}

	job, err := jobService.Get(id, appG.C)
	switch err.(type) {
	case nil:
		appG.Response(http.StatusOK, e.SUCCESS, job)
	case models.NonExistJobError:
		appG.Response(http.StatusNotFound, e.ERROR_NOT_EXIST_JOB, nil)
	default:
		logging.Error(err)
		appG.Response(http.StatusInternalServerError, e.ERROR_GET_JOB_FAIL, nil)
	}
}

// @Router /api/v1/jobs [put]
func SubmitJob(c *gin.Context) {
	appG := app.Gin{C: c}
	reader := http.MaxBytesReader(c.Writer, c.Request.Body, 2000000)
	data, err := io.ReadAll(reader)
	if err != nil {
		logging.Warn(err)
		appG.Response(http.StatusInternalServerError, e.ERROR, nil)
		return
	}

	logging.Infof("Received a file, len: %d", len(data))

	jobService := jobservice.JobService{}

	job, err := jobService.Add(bytes.NewReader(data), appG.C)
	switch err.(type) {
	case nil:
		appG.Response(http.StatusOK, e.SUCCESS, job)
	default:
		logging.Error(err)
		appG.Response(http.StatusInternalServerError, e.ERROR_ADD_JOB_FAIL, nil)
	}
}
