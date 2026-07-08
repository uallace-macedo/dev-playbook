package com.uallace.fixflow_backend.modules.item.controllers.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

public record ItemResponseDTO(
    UUID id,
    String name,
    BigDecimal price,
    Integer quantity,

    @JsonProperty("created_at")
    OffsetDateTime createdAt
) {}
