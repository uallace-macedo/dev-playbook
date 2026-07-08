package com.uallace.fixflow_backend.modules.item.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.ResourceNotFoundException;

public class ItemNotFoundException extends ResourceNotFoundException {
    public ItemNotFoundException(String message) {
        super(message);
    }
}
