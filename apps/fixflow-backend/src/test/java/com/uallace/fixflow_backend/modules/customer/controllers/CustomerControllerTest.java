package com.uallace.fixflow_backend.modules.customer.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTOFixture;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateVehicleDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateVehicleDTOFixture;
import com.uallace.fixflow_backend.modules.customer.controllers.mappers.CustomerMapper;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CpfAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.errors.EmailAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.services.CustomerService;
import com.uallace.fixflow_backend.modules.vehicle.controllers.mappers.VehicleMapper;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import com.uallace.fixflow_backend.shared.exceptions.handler.GlobalExceptionHandler;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mapstruct.factory.Mappers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableHandlerMethodArgumentResolver;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.List;
import java.util.UUID;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
public class CustomerControllerTest {

    @InjectMocks
    CustomerController controller;

    @Mock
    CustomerService customerService;

    @Spy
    CustomerMapper customerMapper = Mappers.getMapper(CustomerMapper.class);

    @Spy
    VehicleMapper vehicleMapper = Mappers.getMapper(VehicleMapper.class);

    MockMvc mockMvc;
    ObjectMapper objectMapper;
    String url = "/api/v1/customers";

    Customer customer;
    CreateCustomerRequestDTO createCustomerRequestDTO;
    Vehicle vehicle;

    @BeforeEach
    void setup() {
        mockMvc = MockMvcBuilders.standaloneSetup(controller)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setCustomArgumentResolvers(new PageableHandlerMethodArgumentResolver())
                .alwaysDo(print())
                .build();

        objectMapper = new ObjectMapper();

        UUID id = UUID.fromString("f9e34a2d-b0a8-48bc-9f4a-8d7b38d6fc3e");
        customer = Customer.builder().id(id).name("customer").email("customer@email.com").phone("(00) 00000-0000").cpf("000.000.000-00").build();
        createCustomerRequestDTO = CreateCustomerRequestDTOFixture.build("customer", "customer@email.com", "(00) 00000-0000", "000.000.000-00");

        vehicle = Vehicle.builder().id(UUID.randomUUID()).licensePlate("AAA0000").make("XX").model("XXXX").year((short) 2010).customer(customer).build();
    }

    @Nested
    @DisplayName("/POST - createCustomer")
    class createCustomer {
        @Test
        @DisplayName("Should create customer successfully")
        void shouldCreateCustomerSuccessfully() throws Exception {
            Mockito.when(customerService.save(Mockito.any(Customer.class))).thenReturn(customer);

            mockMvc.perform(post(url)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(createCustomerRequestDTO)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.name").value("customer"));
        }

        @Test
        @DisplayName("Should return bad request when cpf already exists")
        void shouldReturnBadRequestWhenCpfAlreadyExists() throws Exception {
            Mockito.when(customerService.save(Mockito.any(Customer.class)))
                    .thenThrow(new CpfAlreadyExistsException("CPF já cadastrado"));

            mockMvc.perform(post(url)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(createCustomerRequestDTO)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.message").value("CPF já cadastrado"));
        }

        @Test
        @DisplayName("Should return bad request when email already exists")
        void shouldReturnBadRequestWhenEmailAlreadyExists() throws Exception {
            Mockito.when(customerService.save(Mockito.any(Customer.class)))
                    .thenThrow(new EmailAlreadyExistsException("Email já cadastrado"));

            mockMvc.perform(post(url)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(createCustomerRequestDTO)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.message").value("Email já cadastrado"));
        }
    }

    @Test
    @DisplayName("/GET (findAll) - Should find all customers")
    void shouldFindAllCustomers() throws Exception {
        List<Customer> customerList = List.of(customer);
        Pageable customerPageable = PageRequest.of(0, 20);
        Page<Customer> customerPage = new PageImpl<>(customerList, customerPageable, customerList.size());

        Mockito.when(customerService.findAll(Mockito.any(Pageable.class))).thenReturn(customerPage);
        mockMvc.perform(get(url)
                        .accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.content").isArray())
            .andExpect(jsonPath("$.content[0].name").value("customer"))
            .andExpect(jsonPath("$.totalElements").value(1));
    }

    @Test
    @DisplayName("/GET (findVehicles) - Should find a customer's vehicles")
    void shouldFindACustomersVehiclesSuccessfully() throws Exception {
        List<Vehicle> vehicles = List.of(vehicle);
        Mockito.when(customerService.getVehicles(Mockito.anyString())).thenReturn(vehicles);

        mockMvc.perform(get(url + "/" + customer.getId() + "/vehicles"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray());
    }

    @Test
    @DisplayName("/POST (addVehicle) - Should add vehicle successfully")
    void shouldAddVehicleSuccessfully() throws Exception {
        Mockito.when(customerService.createVehicle(Mockito.anyString(), Mockito.any(Vehicle.class))).thenReturn(vehicle);
        CreateVehicleDTO dto = CreateVehicleDTOFixture.build("AAA0000", "XX", "XXXX", (short) 2010);

        mockMvc.perform(post(url + "/{customerId}/vehicle", customer.getId().toString())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.licensePlate").value(vehicle.getLicensePlate()))
                .andExpect(jsonPath("$.year").value((int) vehicle.getYear()));
    }
}