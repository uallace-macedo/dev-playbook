package com.uallace.fixflow_backend.modules.item.controllers.dto;

import java.math.BigDecimal;

public class UpdateItemDTOFixture {
    public static UpdateItemDTO build() {
        return new UpdateItemDTO(
            "Item Atualizado",
            new BigDecimal("199.99"),
            2
        );
    }

    public static UpdateItemDTO build(String name, BigDecimal price, Integer quantity) {
        return new UpdateItemDTO(name, price, quantity);
    }
}