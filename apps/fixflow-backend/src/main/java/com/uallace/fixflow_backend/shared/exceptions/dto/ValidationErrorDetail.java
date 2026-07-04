package com.uallace.fixflow_backend.shared.exceptions.dto;

public record ValidationErrorDetail(
    String field,
    String message
) {}
