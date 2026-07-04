package com.uallace.fixflow_backend.modules.customer.controllers.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public record CreateCustomerRequestDTO(
    @NotBlank(message = "O nome do cliente é obrigatório")
    String name,

    @NotBlank(message = "O email é obrigatório")
    @Email(message = "O email informado é inválido!")
    String email,

    String phone,

    @NotBlank(message = "O CPF é obrigatório!")
    @Pattern(regexp = "^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$")
    String cpf
) {}
