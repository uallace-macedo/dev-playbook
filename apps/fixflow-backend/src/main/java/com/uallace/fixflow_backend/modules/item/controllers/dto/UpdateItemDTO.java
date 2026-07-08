package com.uallace.fixflow_backend.modules.item.controllers.dto;

import java.math.BigDecimal;

public record UpdateItemDTO(
   String name,
   BigDecimal price,
   Integer quantity
) {}
