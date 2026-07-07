package com.uallace.fixflow_backend.modules.customer.errors;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.ResourceNotFoundException;

import java.util.UUID;

public class CustomerNotFoundException extends ResourceNotFoundException {
    public CustomerNotFoundException(String message) {
        super(message);
    }

    public CustomerNotFoundException(UUID id) {
        super("Cliente de id '" + id.toString() + "' não encontrado!");
    }
}
