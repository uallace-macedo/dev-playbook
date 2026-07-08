package com.uallace.fixflow_backend.modules.item.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class ItemInvalidQuantityException extends BusinessException {
    public ItemInvalidQuantityException(String message) {
        super(message);
    }
}
