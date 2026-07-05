package com.uallace.fixflow_backend.modules.customer.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTOFixture;
import com.uallace.fixflow_backend.modules.customer.controllers.mappers.CustomerMapper;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CpfAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.errors.EmailAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.services.CustomerService;
import com.uallace.fixflow_backend.shared.exceptions.handler.GlobalExceptionHandler;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mapstruct.factory.Mappers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy; // Importamos o Spy
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableHandlerMethodArgumentResolver;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.List;
import java.util.UUID;

import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;

@ExtendWith(MockitoExtension.class)
public class CustomerControllerTest {

    @InjectMocks
    CustomerController controller;

    @Mock
    CustomerService customerService;

    @Spy
    CustomerMapper customerMapper = Mappers.getMapper(CustomerMapper.class);

    MockMvc mockMvc;
    ObjectMapper objectMapper;
    String url = "/api/v1/customers";

    Customer customer;
    CreateCustomerRequestDTO createCustomerRequestDTO;

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
    }

    @Test
    void shouldCreateCustomerSuccessfully() throws Exception {
        Mockito.when(customerService.save(Mockito.any(Customer.class))).thenReturn(customer);

        mockMvc.perform(MockMvcRequestBuilders.post(url)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(createCustomerRequestDTO)))
                .andExpect(MockMvcResultMatchers.status().isCreated())
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("customer"));
    }

    @Test
    void shouldFindAllCustomers() throws Exception {
        List<Customer> customerList = List.of(customer);
        Pageable customerPageable = PageRequest.of(0, 20);
        Page<Customer> customerPage = new PageImpl<>(customerList, customerPageable, customerList.size());

        Mockito.when(customerService.findAll(Mockito.any(Pageable.class))).thenReturn(customerPage);
        mockMvc.perform(MockMvcRequestBuilders
                        .get(url)
                        .accept(MediaType.APPLICATION_JSON)
        )
            .andExpect(MockMvcResultMatchers.status().isOk())
            .andExpect(MockMvcResultMatchers.jsonPath("$.content").isArray())
            .andExpect(MockMvcResultMatchers.jsonPath("$.content[0].name").value("customer"))
            .andExpect(MockMvcResultMatchers.jsonPath("$.totalElements").value(1));
    }

    @Test
    void shouldReturnBadRequestWhenCpfAlreadyExists() throws Exception {
        Mockito.when(customerService.save(Mockito.any(Customer.class)))
                .thenThrow(new CpfAlreadyExistsException("CPF já cadastrado"));

        mockMvc.perform(MockMvcRequestBuilders.post(url)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(createCustomerRequestDTO)))
                .andExpect(MockMvcResultMatchers.status().isBadRequest())
                .andExpect(MockMvcResultMatchers.jsonPath("$.message").value("CPF já cadastrado"));
    }

    @Test
    void shouldReturnBadRequestWhenEmailAlreadyExists() throws Exception {
        Mockito.when(customerService.save(Mockito.any(Customer.class)))
                .thenThrow(new EmailAlreadyExistsException("Email já cadastrado"));

        mockMvc.perform(MockMvcRequestBuilders.post(url)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(createCustomerRequestDTO)))
                .andExpect(MockMvcResultMatchers.status().isBadRequest())
                .andExpect(MockMvcResultMatchers.jsonPath("$.message").value("Email já cadastrado"));
    }
}