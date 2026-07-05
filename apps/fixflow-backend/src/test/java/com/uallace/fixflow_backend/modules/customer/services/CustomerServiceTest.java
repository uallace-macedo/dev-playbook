package com.uallace.fixflow_backend.modules.customer.services;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CpfAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.errors.EmailAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.repositories.CustomerRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class CustomerServiceTest {
    @InjectMocks
    CustomerService customerService;

    @Mock
    CustomerRepository customerRepository;

    Customer customer;
    Pageable customerPageable;
    Page<Customer> customerPage;

    @BeforeEach
    void setup() {
        customer = Customer.builder().name("customer").email("customer@email.com").phone("(00) 00000-0000").cpf("000.000.000-00").build();

        List<Customer> customerList = List.of(customer);
        customerPageable = PageRequest.of(0, 10);
        customerPage = new PageImpl<>(customerList, customerPageable, customerList.size());
    }

    @Test
    void shouldSaveSuccessfully() {
        Mockito.when(customerRepository.save(customer)).thenReturn(customer);

        Customer actual = customerRepository.save(customer);
        Assertions.assertEquals(customer, actual);

        Mockito.verify(customerRepository, Mockito.times(1)).save(customer);
        Mockito.verifyNoMoreInteractions(customerRepository);
    }

    @Test
    void shouldReturnCustomersPage() {
        Mockito.when(customerService.findAll(customerPageable)).thenReturn(customerPage);

        Page<Customer> actual = customerService.findAll(customerPageable);

        Assertions.assertNotNull(actual);
        Assertions.assertEquals(customerPage, actual);
        Assertions.assertEquals(1, actual.getTotalElements(), "Should have only 1 element on pagination");
        Assertions.assertEquals("customer", actual.getContent().getFirst().getName());

        Mockito.verify(customerRepository, Mockito.times(1)).findAll(customerPageable);
        Mockito.verifyNoMoreInteractions(customerRepository);
    }

    @Test
    void shouldThrowCpfAlreadyExistsException() {
        Mockito.when(customerRepository.findByCpf("000.000.000-00")).thenReturn(Optional.of(customer));

        CpfAlreadyExistsException ex = Assertions.assertThrows(
            CpfAlreadyExistsException.class,
            () -> customerService.save(customer)
        );

        Assertions.assertNotNull(ex);
        Assertions.assertEquals("CPF já cadastrado", ex.getMessage());

        Mockito.verify(customerRepository, Mockito.never()).save(Mockito.any());
    }

    @Test
    void shouldThrowEmailAlreadyExistsException() {
        Mockito.when(customerRepository.findByEmail("customer@email.com")).thenReturn(Optional.of(customer));

        EmailAlreadyExistsException ex = Assertions.assertThrows(
            EmailAlreadyExistsException.class,
            () -> customerService.save(customer)
        );

        Assertions.assertNotNull(ex);
        Assertions.assertEquals("Email já cadastrado", ex.getMessage());

        Mockito.verify(customerRepository, Mockito.never()).save(Mockito.any());
    }
}
