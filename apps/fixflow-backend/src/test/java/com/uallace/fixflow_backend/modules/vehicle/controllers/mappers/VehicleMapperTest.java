package com.uallace.fixflow_backend.modules.vehicle.controllers.mappers;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTOFixture;
import com.uallace.fixflow_backend.modules.customer.controllers.mappers.CustomerMapper;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.*;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mapstruct.factory.Mappers;
import org.mockito.InjectMocks;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.UUID;

@ExtendWith(MockitoExtension.class)
public class VehicleMapperTest {

    @Spy
    CustomerMapper customerMapper = Mappers.getMapper(CustomerMapper.class);

    @InjectMocks
    VehicleMapper vehicleMapper = Mappers.getMapper(VehicleMapper.class);

    Customer customer;
    CustomerResponseDTO customerResponseDTO;

    Vehicle vehicle;
    VehicleResponseDTO vehicleResponseDTO;
    VehicleCompleteResponseDTO vehicleCompleteResponseDTO;
    CreateVehicleDTO createVehicleDTO;

    @BeforeEach
    void setup() {
        UUID vehicleUUID = UUID.fromString("3d9a2ff1-e2ca-499f-9fc6-926d83cf9fb3");
        UUID customerUUID = UUID.fromString("86f59571-3e05-4c87-b714-5d6affdb20e8");

        customer = Customer.builder().id(customerUUID).name("customer").email("customer@email.com").phone("(00) 00000-0000").cpf("000.000.000-00").build();
        customerResponseDTO = CustomerResponseDTOFixture.build(customerUUID, "customer", "customer@email.com", "(00) 00000-0000", "000.000.000-00");
        vehicle = Vehicle.builder().id(vehicleUUID).customer(customer).licensePlate("AAA0000").make("VW").model("GOL").year((short) 2010).build();

        vehicleResponseDTO = VehicleResponseDTOFixture.build(vehicleUUID, "AAA0000", "VW", "GOL", (short) 2010, null);
        vehicleCompleteResponseDTO = VehicleCompleteResponseDTOFixture.build(vehicleUUID, customerResponseDTO, "AAA0000", "VW", "GOL", (short) 2010, null);
        createVehicleDTO = CreateVehicleDTOFixture.build(customerUUID, "AAA0000", "VW", "GOL", (short) 2010);
    }

    @Test
    void shouldConvertToDTOSuccessfully() {
        VehicleResponseDTO actualVehicleResponseDTO = vehicleMapper.toDTO(vehicle);
        VehicleCompleteResponseDTO actualVehicleCompleteResponseDTO = vehicleMapper.toCompleteDTO(vehicle);

        Assertions.assertEquals(vehicleResponseDTO, actualVehicleResponseDTO);
        Assertions.assertEquals(vehicleCompleteResponseDTO, actualVehicleCompleteResponseDTO);
    }

    @Test
    void shouldConvertToEntitySuccessfully() {
        Vehicle expectedVehicle = vehicleMapper.toEntity(createVehicleDTO);

        Assertions.assertAll(
            () -> Assertions.assertNull(expectedVehicle.getId()),
            () -> Assertions.assertEquals(vehicle.getLicensePlate(), expectedVehicle.getLicensePlate()),
            () -> Assertions.assertEquals(vehicle.getYear(), expectedVehicle.getYear())
        );
    }
}
