package com.uallace.fixflow_backend.modules.item.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class ItemNameAlreadyExistsException extends BusinessException {
    public ItemNameAlreadyExistsException(String name) {
        super("Já existe um item com nome '" + name + "'!");
    }
}
