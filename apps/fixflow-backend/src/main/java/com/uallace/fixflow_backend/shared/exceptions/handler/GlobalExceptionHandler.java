package com.uallace.fixflow_backend.shared.exceptions.handler;

import com.uallace.fixflow_backend.shared.exceptions.dto.ExceptionResponse;
import com.uallace.fixflow_backend.shared.exceptions.dto.ValidationErrorDetail;
import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;
import com.uallace.fixflow_backend.shared.exceptions.exceptions.ResourceNotFoundException;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.List;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ExceptionResponse> handleValidationExceptions(MethodArgumentNotValidException ex, HttpServletRequest req) {
        List<ValidationErrorDetail> errors = ex.getBindingResult().getFieldErrors()
                .stream().map(
                        err -> new ValidationErrorDetail(err.getField(), err.getDefaultMessage())
                ).toList();

        ExceptionResponse response = new ExceptionResponse(
                Instant.now(),
                req.getContextPath(),
                "Dados inválidos",
                errors
        );

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ExceptionResponse> handleBusinessExceptions(BusinessException ex, HttpServletRequest req) {
        ExceptionResponse response = new ExceptionResponse(
                Instant.now(),
                req.getRequestURI(),
                "Dado inválido",
                ex.getMessage()
        );

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ExceptionResponse> handleResourceNotFoundExceptions(ResourceNotFoundException ex, HttpServletRequest req) {
        ExceptionResponse response = new ExceptionResponse(
                Instant.now(),
                req.getRequestURI(),
                "Recurso não encontrado",
                ex.getMessage()
        );

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ExceptionResponse> handleExceptions(Exception ex, HttpServletRequest req) {
        ExceptionResponse response = new ExceptionResponse(
                Instant.now(),
                req.getRequestURI(),
                "Erro inesperado",
                ex.getMessage()
        );

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
