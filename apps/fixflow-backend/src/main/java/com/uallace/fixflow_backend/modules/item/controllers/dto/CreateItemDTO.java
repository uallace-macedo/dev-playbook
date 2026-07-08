package com.uallace.fixflow_backend.modules.item.controllers.dto;

import com.uallace.fixflow_backend.modules.item.entities.ItemType;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.validator.constraints.Length;

import java.math.BigDecimal;

public record CreateItemDTO(
    @NotBlank(message = "Nome do item é obrigatório!")
    @Length(min = 2 ,message = "Nome do item precisa conter no mínimo 2 caracteres!")
    String name,

    @NotNull(message = "O preço é obrigatório!")
    @Min(value = 1, message = "O preço deve ser no mínimo 1!")
    BigDecimal price,

    @NotNull(message = "O tipo do item é obrigatório: <PART,SERVICE>")
    ItemType type
) {}
