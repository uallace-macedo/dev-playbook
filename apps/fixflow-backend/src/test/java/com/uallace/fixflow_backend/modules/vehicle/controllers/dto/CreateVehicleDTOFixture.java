package com.uallace.fixflow_backend.modules.vehicle.controllers.dto;

import java.util.UUID;

public class CreateVehicleDTOFixture {
    public static CreateVehicleDTO build() {
        return new CreateVehicleDTO(
                UUID.randomUUID(),
                "AAA0000",
                "XX",
                "XXXX",
                (short) 2010
        );
    }

    public static CreateVehicleDTO build(UUID customerId, String licensePlate, String make, String model, short year) {
        return new CreateVehicleDTO(customerId, licensePlate, make, model, year);
    }
}
