package com.uallace.fixflow_backend.modules.customer.controllers;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.mappers.CustomerMapper;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.services.CustomerService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/customers")
@RequiredArgsConstructor
public class CustomerController {
    private final CustomerService customerService;
    private final CustomerMapper customerMapper;

    @PostMapping("")
    public ResponseEntity<?> createCustomer(@Valid @RequestBody CreateCustomerRequestDTO customerData) {
        Customer savedCustomer = customerService.save(
                customerMapper.toEntity(customerData)
        );

        return ResponseEntity.status(HttpStatus.CREATED).body(customerMapper.toDTO(savedCustomer));
    }

    @GetMapping("")
    public ResponseEntity<?> findAll(@PageableDefault(page = 0, size = 20) Pageable pageable) {
        Page<CustomerResponseDTO> dtoPage = customerService.findAll(pageable).map(customerMapper::toDTO);
        return ResponseEntity.status(HttpStatus.OK).body(dtoPage);
    }
}
