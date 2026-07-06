package com.uallace.fixflow_backend.modules.vehicle.controllers.dto;

import java.time.OffsetDateTime;
import java.util.UUID;

public record VehicleResponseDTO(
    UUID id,
    String licensePlate,
    String make,
    String model,
    short year,
    OffsetDateTime createdAt
) {}
