package com.uallace.fixflow_backend.modules.item.controllers.dto;

import java.math.BigDecimal;

public class CreateItemDTOFixture {
    public static CreateItemDTO build() {
        return new CreateItemDTO(
            "Item Padrão",
            new BigDecimal("99.90"),
            10
        );
    }

    public static CreateItemDTO build(String name, BigDecimal price, Integer quantity) {
        return new CreateItemDTO(name, price, quantity);
    }
}