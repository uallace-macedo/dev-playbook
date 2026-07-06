package com.uallace.fixflow_backend.modules.vehicle.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class LicensePlateAlreadyExistsException extends BusinessException {
    public LicensePlateAlreadyExistsException(String message) {
        super(message);
    }
}
