package com.uallace.fixflow_backend.modules.vehicle.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.BusinessException;

public class InvalidVehicleYearException extends BusinessException {
    public InvalidVehicleYearException(String message) {
        super(message);
    }
}
