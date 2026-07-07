package com.uallace.fixflow_backend.modules.vehicle.exceptions;

import com.uallace.fixflow_backend.shared.exceptions.exceptions.ResourceNotFoundException;

public class VehicleNotFoundException extends ResourceNotFoundException {
    public VehicleNotFoundException(String message) {
        super(message);
    }
}
