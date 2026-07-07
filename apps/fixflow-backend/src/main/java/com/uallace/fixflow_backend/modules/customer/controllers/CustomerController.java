package com.uallace.fixflow_backend.modules.customer.controllers;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateVehicleDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.mappers.CustomerMapper;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.services.CustomerService;
import com.uallace.fixflow_backend.modules.vehicle.controllers.mappers.VehicleMapper;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
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
    private final VehicleMapper vehicleMapper;

    @GetMapping("")
    public ResponseEntity<?> findAll(@PageableDefault(page = 0, size = 20) Pageable pageable) {
        Page<CustomerResponseDTO> dtoPage = customerService.findAll(pageable).map(customerMapper::toDTO);
        return ResponseEntity.status(HttpStatus.OK).body(dtoPage);
    }

    @GetMapping("/{customerId}/vehicles")
    public ResponseEntity<?> findVehicles(@PathVariable("customerId") String customerId) {
        return ResponseEntity.status(HttpStatus.OK).body(
                vehicleMapper.toDTO(customerService.getVehicles(customerId))
        );
    }

    @PostMapping("")
    public ResponseEntity<?> createCustomer(@Valid @RequestBody CreateCustomerRequestDTO customerData) {
        Customer savedCustomer = customerService.save(
                customerMapper.toEntity(customerData)
        );

        return ResponseEntity.status(HttpStatus.CREATED).body(customerMapper.toDTO(savedCustomer));
    }

    @PostMapping("/{customerId}/vehicle")
    public ResponseEntity<?> addVehicle(@PathVariable("customerId") String customerId, @Valid @RequestBody CreateVehicleDTO vehicleDTO) {
        Vehicle vehicle = vehicleMapper.toEntity(vehicleDTO);
        return ResponseEntity.status(HttpStatus.CREATED).body(
            vehicleMapper.toDTO(customerService.createVehicle(customerId, vehicle))
        );
    }
}
