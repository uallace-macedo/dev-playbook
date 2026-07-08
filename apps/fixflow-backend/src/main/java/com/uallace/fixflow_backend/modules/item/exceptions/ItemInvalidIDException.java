package com.uallace.fixflow_backend.modules.item.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class ItemInvalidIDException extends BusinessException {
    public ItemInvalidIDException(String message) {
        super(message);
    }
}
