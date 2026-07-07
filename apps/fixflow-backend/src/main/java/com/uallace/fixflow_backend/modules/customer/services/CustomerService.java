package com.uallace.fixflow_backend.modules.customer.services;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CpfAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.errors.CustomerNotFoundException;
import com.uallace.fixflow_backend.modules.customer.errors.EmailAlreadyExistsException;
import com.uallace.fixflow_backend.modules.customer.errors.InvalidCustomerIdException;
import com.uallace.fixflow_backend.modules.customer.repositories.CustomerRepository;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.InvalidVehicleYearException;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.LicensePlateAlreadyExistsException;
import com.uallace.fixflow_backend.modules.vehicle.repositories.VehicleRepository;
import com.uallace.fixflow_backend.modules.vehicle.services.VehicleService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Year;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class CustomerService {
    private final CustomerRepository customerRepository;
    private final VehicleService vehicleService;

    public Customer save(Customer customer) {
        if(customerRepository.findByCpf(customer.getCpf()).isPresent()) throw new CpfAlreadyExistsException("CPF já cadastrado");
        if(customerRepository.findByEmail(customer.getEmail()).isPresent()) throw new EmailAlreadyExistsException("Email já cadastrado");

        return customerRepository.save(customer);
    }

    public Page<Customer> findAll(Pageable pageable) {
        return customerRepository.findAll(pageable);
    }

    public List<Vehicle> getVehicles(String customerId) {
        UUID id = verifyUUID(customerId);
        if(!customerRepository.existsById(id)) throw new CustomerNotFoundException(id);
        return vehicleService.findByCustomerId(id);
    }

    public Vehicle createVehicle(String customerId, Vehicle vehicle) {
        UUID id = verifyUUID(customerId);
        return vehicleService.save(id, vehicle);
    }

    private UUID verifyUUID(String id) {
        try {
            return UUID.fromString(id);
        } catch (IllegalArgumentException ex) {
            throw new InvalidCustomerIdException("Por favor, informe um ID de cliente válido!");
        }
    }
}
