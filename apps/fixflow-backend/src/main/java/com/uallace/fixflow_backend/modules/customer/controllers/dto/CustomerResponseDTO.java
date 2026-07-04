package com.uallace.fixflow_backend.modules.customer.controllers.dto;

import java.util.UUID;

public record CustomerResponseDTO(
    UUID id,
    String name,
    String email,
    String phone,
    String cpf
) {}
