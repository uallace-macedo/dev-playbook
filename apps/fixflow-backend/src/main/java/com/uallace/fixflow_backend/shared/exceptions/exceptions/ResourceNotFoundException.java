package com.uallace.fixflow_backend.shared.exceptions.exceptions;

public abstract class ResourceNotFoundException extends RuntimeException {
    protected ResourceNotFoundException(String message) {
        super(message);
    }
}
