package com.uallace.fixflow_backend.modules.customer.errors;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class InvalidCustomerIdException extends BusinessException {
    public InvalidCustomerIdException(String message) {
        super(message);
    }
}
