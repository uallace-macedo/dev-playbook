package com.uallace.fixflow_backend.modules.customer.errors;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.ResourceNotFoundException;

public class CustomerNotFoundException extends ResourceNotFoundException {
    public CustomerNotFoundException(String message) {
        super(message);
    }
}
