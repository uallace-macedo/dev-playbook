package user

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/dto"
)

func (h *Handler) Register(c *gin.Context) {
	var (
		ctx = c.Request.Context()
		req dto.RegisterRequest
	)

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"success": false,
			"message": "please provide all data",
		})

		return
	}

	userdID, statusCode, err := h.userService.Register(ctx, &req)
	if err != nil {
		c.JSON(statusCode, gin.H{
			"success": false,
			"message": err.Error(),
		})

		return
	}

	c.JSON(statusCode, gin.H{
		"success": true,
		"ID":      userdID,
	})
}
