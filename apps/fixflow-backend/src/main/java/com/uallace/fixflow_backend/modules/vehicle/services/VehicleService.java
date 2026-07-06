package com.uallace.fixflow_backend.modules.vehicle.services;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CustomerNotFoundException;
import com.uallace.fixflow_backend.modules.customer.repositories.CustomerRepository;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.InvalidVehicleYearException;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.LicensePlateAlreadyExistsException;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.VehicleNotFoundException;
import com.uallace.fixflow_backend.modules.vehicle.repositories.VehicleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Year;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class VehicleService {
    private final VehicleRepository vehicleRepository;
    private final CustomerRepository customerRepository;

    public Page<Vehicle> findAll(Pageable pageable) {
        return vehicleRepository.findAll(pageable);
    }

    public Vehicle save(UUID customerId, Vehicle vehicle) {
        Customer customer = customerRepository.findById(customerId).orElseThrow(() -> new CustomerNotFoundException("Cliente de id '" + customerId + "' não foi encontrado."));
        if(vehicleRepository.existsByLicensePlate(vehicle.getLicensePlate())) throw new LicensePlateAlreadyExistsException("Placa '" + vehicle.getLicensePlate() + "' já está cadastrada!");
        if(1880 > vehicle.getYear() || vehicle.getYear() > (Year.now().getValue() + 1)) throw new InvalidVehicleYearException("O ano do veículo deve estar entre 1880 e " + (Year.now().getValue() + 1));

        vehicle.setCustomer(customer);
        return vehicleRepository.save(vehicle);
    }

    public Vehicle findById(UUID vehicleId) {
        return vehicleRepository.findById(vehicleId).orElseThrow(() -> new VehicleNotFoundException("Veículo com id '" + vehicleId + "' não foi encontrado."));
    }

    public Vehicle findByLicensePlate(String licensePlate) {
        return vehicleRepository.findByLicensePlate(licensePlate).orElseThrow(() -> new VehicleNotFoundException("Veículo com placa '" + licensePlate + "' não foi encontrado."));
    }
}
