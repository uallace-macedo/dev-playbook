package com.uallace.fixflow_backend.modules.customer.controllers.dto;

import java.util.UUID;

public class CustomerResponseDTOFixture {
    public static CustomerResponseDTO build() {
        return new CustomerResponseDTO(
                UUID.fromString("d4b8e239-16a7-47c3-a3d5-d86b86d634ea"),
                "Customer-name",
                "Customer-email",
                "Customer-phone",
                "Customer-cpf"
        );
    }

    public static CustomerResponseDTO build(UUID id, String name, String email, String phone, String cpf) {
        return new CustomerResponseDTO(id, name, email, phone, cpf);
    }
}
