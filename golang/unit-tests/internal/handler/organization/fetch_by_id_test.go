package organization

import (
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/labstack/echo/v4"
	mocks "github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/mocks/organization"
	"github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/model/organization"
	"go.uber.org/mock/gomock"
)

func Test_FetchById(t *testing.T) {
	e := echo.New()
	ctrl := gomock.NewController(t)

	repositoryMock := mocks.NewMockOrganizationRepository(ctrl)
	organizationHandler := NewOrganizationHandler(repositoryMock)

	testCases := []struct {
		name           string
		id             string
		setupMocks     func()
		expectedStatus int
		expectError    bool
	}{
		{
			name:           "when id is null, return bad request",
			setupMocks:     func() {},
			expectedStatus: http.StatusBadRequest,
			expectError:    true,
		},
		{
			name: "when fetchById fails, return internal server errors",
			id:   "123",
			setupMocks: func() {
				repositoryMock.EXPECT().FetchById(gomock.Any(), "123").Return(&organization.OrganizationModel{}, errors.New("error"))
			},
			expectError:    true,
			expectedStatus: http.StatusInternalServerError,
		},
		{
			name: "when doesnt have any errors, return OK",
			id:   "123",
			setupMocks: func() {
				repositoryMock.EXPECT().FetchById(gomock.Any(), "123").Return(&organization.OrganizationModel{}, nil)
			},
			expectError:    false,
			expectedStatus: http.StatusOK,
		},
	}

	for _, tt := range testCases {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodGet, "/organization/:id", nil)
			rec := httptest.NewRecorder()
			echoContext := e.NewContext(req, rec)

			echoContext.SetParamNames("id")
			echoContext.SetParamValues(tt.id)

			tt.setupMocks()

			err := organizationHandler.FetchById(echoContext)
			if err != nil && !tt.expectError {
				t.Error(err)
			}

			if tt.expectedStatus != rec.Code {
				t.Errorf("expected status: %d, received status: %d", tt.expectedStatus, rec.Code)
			}
		})
	}

}
