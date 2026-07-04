package com.uallace.fixflow_backend.shared.exceptions.exceptions;

public abstract class BusinessException extends RuntimeException {
    protected BusinessException(String message) {
        super(message);
    }
}
