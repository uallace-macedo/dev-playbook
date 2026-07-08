package com.uallace.fixflow_backend.shared.exceptions.handler;

import com.fasterxml.jackson.databind.exc.InvalidFormatException;
import com.fasterxml.jackson.databind.exc.MismatchedInputException;
import com.uallace.fixflow_backend.modules.item.entities.ItemType;
import com.uallace.fixflow_backend.shared.exceptions.dto.ExceptionResponse;
import com.uallace.fixflow_backend.shared.exceptions.dto.ValidationErrorDetail;
import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;
import com.uallace.fixflow_backend.shared.exceptions.exceptions.ResourceNotFoundException;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

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

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ExceptionResponse> handleHttpMessageNotReadableExceptions(HttpMessageNotReadableException ex, HttpServletRequest req) {
        StringBuilder message = new StringBuilder("Tipo inválido. Tipos permitidos: ");

        if(ex.getCause() instanceof InvalidFormatException || ex.getCause() instanceof MismatchedInputException) {
            var cause = ex.getCause();
            if(cause.getLocalizedMessage().contains("ItemType")) {
                String allowedTypes = Arrays.stream(ItemType.values())
                        .map(Enum::name)
                        .collect(Collectors.joining(", "));

                message.append(allowedTypes);
            }
        }

        ExceptionResponse response = new ExceptionResponse(
                Instant.now(),
                req.getRequestURI(),
                "Tipo inválido",
                message
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
