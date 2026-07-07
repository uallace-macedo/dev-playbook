package com.uallace.fixflow_backend.modules.customer.controllers.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.validator.constraints.Length;

public record CreateVehicleDTO(
        @JsonProperty("license_plate")
        @NotBlank(message = "Por favor, informe a placa do veículo!")
        @Length(min = 7, max = 15, message = "A placa do veículo deve conter de 7 a 15 caracteres!")
        String licensePlate,

        @NotBlank(message = "Por favor, informe a marca do veículo!")
        String make,

        @NotBlank(message = "Por favor, informe o modelo do veículo!")
        String model,

        @NotNull(message = "Por favor, informe o ano do veículo!")
        short year
) {}
