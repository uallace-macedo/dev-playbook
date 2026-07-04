package com.uallace.fixflow_backend.modules.customer.errors;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class CpfAlreadyExistsException extends BusinessException {
    public CpfAlreadyExistsException(String message) {
        super(message);
    }
}
