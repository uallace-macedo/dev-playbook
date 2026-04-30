package organization

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (h *organizationHandler) FetchById(c echo.Context) error {
	id := c.Param("id")

	if id == "" {
		return c.String(http.StatusBadRequest, "please provide a valid id")
	}

	organization, err := h.repo.FetchById(c.Request().Context(), id)
	if err != nil {
		return c.String(http.StatusInternalServerError, err.Error())
	}

	return c.JSON(http.StatusOK, organization)
}
