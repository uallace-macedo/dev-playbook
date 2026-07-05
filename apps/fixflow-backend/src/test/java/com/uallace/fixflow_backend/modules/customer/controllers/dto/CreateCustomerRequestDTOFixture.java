package com.uallace.fixflow_backend.modules.customer.controllers.dto;

public class CreateCustomerRequestDTOFixture {
    public static CreateCustomerRequestDTO build() {
        return new CreateCustomerRequestDTO(
                "User 0",
                "user.0@email.com",
                "(00) 00000-0000",
                "000.000.000-00"
        );
    }

    public static CreateCustomerRequestDTO build(
        String name,
        String email,
        String phone,
        String cpf
    ) {
        return new CreateCustomerRequestDTO(name, email, phone, cpf);
    }
}
