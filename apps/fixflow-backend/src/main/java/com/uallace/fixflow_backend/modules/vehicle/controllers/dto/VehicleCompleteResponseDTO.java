package com.uallace.fixflow_backend.modules.vehicle.controllers.dto;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;

import java.time.OffsetDateTime;
import java.util.UUID;

public record VehicleCompleteResponseDTO(
    UUID id,
    CustomerResponseDTO customer,
    String licensePlate,
    String make,
    String model,
    short year,
    OffsetDateTime createdAt
) {}
