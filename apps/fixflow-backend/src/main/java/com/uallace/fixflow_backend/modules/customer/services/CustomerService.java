package com.uallace.fixflow_backend.modules.customer.services;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CpfAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.errors.EmailAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.repositories.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CustomerService {
    private final CustomerRepository customerRepository;

    public Customer save(Customer customer) {
        if(customerRepository.findByCpf(customer.getCpf()).isPresent()) throw new CpfAlreadyExistsException("CPF já cadastrado");
        if(customerRepository.findByEmail(customer.getEmail()).isPresent()) throw new EmailAlreadyExistsException("Email já cadastrado");

        return customerRepository.save(customer);
    }

    public Page<Customer> findAll(Pageable pageable) {
        return customerRepository.findAll(pageable);
    }
}
