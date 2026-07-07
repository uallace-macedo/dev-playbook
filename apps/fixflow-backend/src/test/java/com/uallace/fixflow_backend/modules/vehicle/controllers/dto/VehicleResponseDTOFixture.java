package com.uallace.fixflow_backend.modules.vehicle.controllers.dto;

import java.time.OffsetDateTime;
import java.util.UUID;

public class VehicleResponseDTOFixture {
    public static VehicleResponseDTO build() {
        return new VehicleResponseDTO(
                UUID.randomUUID(),
                "AAA0000",
                "XX",
                "XXXX",
                (short) 2010,
                OffsetDateTime.now()
        );
    }

    public static VehicleResponseDTO build(UUID id, String licensePlate, String make, String model, short year, OffsetDateTime createdAt) {
        return new VehicleResponseDTO(id, licensePlate, make, model, year, createdAt);
    }
}
