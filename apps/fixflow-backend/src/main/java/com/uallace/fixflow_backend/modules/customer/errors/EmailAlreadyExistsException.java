package com.uallace.fixflow_backend.modules.customer.errors;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class EmailAlreadyExistsException extends BusinessException {
    public EmailAlreadyExistsException(String message) {
        super(message);
    }
}
