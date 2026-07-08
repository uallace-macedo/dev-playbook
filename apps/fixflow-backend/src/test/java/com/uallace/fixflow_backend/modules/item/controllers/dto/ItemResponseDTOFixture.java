package com.uallace.fixflow_backend.modules.item.controllers.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

public class ItemResponseDTOFixture {
    public static ItemResponseDTO build() {
        return new ItemResponseDTO(
            UUID.randomUUID(),
            "Item Cadastrado",
            new BigDecimal("150.00"),
            5,
            OffsetDateTime.now()
        );
    }

    public static ItemResponseDTO build(UUID id, String name, BigDecimal price, Integer quantity, OffsetDateTime createdAt) {
        return new ItemResponseDTO(id, name, price, quantity, createdAt);
    }
}