package com.uallace.fixflow_backend.modules.vehicle.controllers.dto;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTOFixture;

import java.time.OffsetDateTime;
import java.util.UUID;

public class VehicleCompleteResponseDTOFixture {
    public static VehicleCompleteResponseDTO build() {
        return new VehicleCompleteResponseDTO(
                UUID.randomUUID(),
                CustomerResponseDTOFixture.build(),
                "AAA0000",
                "XX",
                "XXXX",
                (short) 2010,
                OffsetDateTime.now()
        );
    }

    public static VehicleCompleteResponseDTO build(UUID id, CustomerResponseDTO customer, String licensePlate, String make, String model, short year, OffsetDateTime createdAt) {
        return new VehicleCompleteResponseDTO(id, customer, licensePlate, make, model, year, createdAt);
    }
}
