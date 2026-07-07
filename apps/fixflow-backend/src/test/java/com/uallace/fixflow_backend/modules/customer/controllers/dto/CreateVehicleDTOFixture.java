package com.uallace.fixflow_backend.modules.customer.controllers.dto;

public class CreateVehicleDTOFixture {
    public static CreateVehicleDTO build() {
        return new CreateVehicleDTO("AAA0000", "XX", "XXXX", (short) 2010);
    }

    public static CreateVehicleDTO build(String licensePlate, String make, String model, short year) {
        return new CreateVehicleDTO(licensePlate, make, model, year);
    }
}
