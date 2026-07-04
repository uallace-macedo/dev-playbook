package com.uallace.fixflow_backend.shared.exceptions.dto;

import java.time.Instant;

public record ExceptionResponse(
    Instant timestamp,
    String path,
    String error,
    Object message
) {}
