package com.uallace.fixflow_backend.modules.customer.controllers.mappers;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTOFixture;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTOFixture;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mapstruct.factory.Mappers;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.UUID;

@ExtendWith(MockitoExtension.class)
public class CustomerMapperTest {
    CustomerMapper customerMapper;

    UUID id;
    Customer customer;
    CustomerResponseDTO responseDTO;
    CreateCustomerRequestDTO customerRequestDTO;

    @BeforeEach
    void setup() {
        customerMapper = Mappers.getMapper(CustomerMapper.class);
        id = UUID.fromString("d4b8e239-16a7-47c3-a3d5-d86b86d634ea");

        customer = Customer.builder().id(id).name("customer 1").email("customer@email.com").phone("(00) 00000-0000").cpf("000.000.000-00").build();
        responseDTO = CustomerResponseDTOFixture.build(id, "customer 1", "customer@email.com", "(00) 00000-0000", "000.000.000-00");
        customerRequestDTO = CreateCustomerRequestDTOFixture.build("customer 1", "customer@email.com", "(00) 00000-0000", "000.000.000-00");
    }

    @Test
    void shouldConvertToCustomerResponseDTO() {
        CustomerResponseDTO actual = customerMapper.toDTO(customer);
        Assertions.assertEquals(responseDTO, actual);
    }

    @Test
    void shouldConvertToCustomer() {
        Customer actual = customerMapper.toEntity(customerRequestDTO);
        Assertions.assertAll(
                () -> Assertions.assertNull(actual.getId()),
                () -> Assertions.assertEquals(customer.getName(), actual.getName()),
                () -> Assertions.assertEquals(customer.getEmail(), actual.getEmail()),
                () -> Assertions.assertEquals(customer.getPhone(), actual.getPhone()),
                () -> Assertions.assertEquals(customer.getCpf(), actual.getCpf())
        );
    }
}
