package com.uallace.fixflow_backend.modules.vehicle.services;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import com.uallace.fixflow_backend.modules.customer.errors.CustomerNotFoundException;
import com.uallace.fixflow_backend.modules.customer.repositories.CustomerRepository;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.InvalidVehicleYearException;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.LicensePlateAlreadyExistsException;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.VehicleNotFoundException;
import com.uallace.fixflow_backend.modules.vehicle.repositories.VehicleRepository;
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

import java.time.Year;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@ExtendWith(MockitoExtension.class)
public class VehicleServiceTest {
    @InjectMocks
    VehicleService vehicleService;

    @Mock
    VehicleRepository vehicleRepository;

    @Mock
    CustomerRepository customerRepository;

    Customer customer;
    Vehicle vehicle;

    Pageable vehiclePageable;
    Page<Vehicle> vehiclePage;

    @BeforeEach
    void setup() {
        UUID customerUUID = UUID.fromString("86f59571-3e05-4c87-b714-5d6affdb20e8");
        UUID vehicleUUID = UUID.fromString("3d9a2ff1-e2ca-499f-9fc6-926d83cf9fb3");

        customer = Customer.builder().id(customerUUID).name("customer").email("customer@email.com").phone("(00) 00000-0000").cpf("000.000.000-00").build();
        vehicle = Vehicle.builder().id(vehicleUUID).customer(customer).licensePlate("AAA0000").make("VW").model("GOL").year((short) 2010).build();

        vehiclePageable = PageRequest.of(0, 20);
        vehiclePage = new PageImpl<Vehicle>(List.of(vehicle), vehiclePageable, 1);
    }

    @Test
    void shouldReturnVehiclePage() {
        Mockito.when(vehicleRepository.findAll(Mockito.any(Pageable.class))).thenReturn(vehiclePage);
        Page<Vehicle> response = vehicleService.findAll(vehiclePageable);

        Assertions.assertEquals(1, response.getContent().size());
        Assertions.assertEquals("AAA0000", response.getContent().getFirst().getLicensePlate());

        Mockito.verify(vehicleRepository, Mockito.times(1)).findAll(Mockito.any(Pageable.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldSaveVehicleSuccessfully() {
        Mockito.when(customerRepository.findById(Mockito.any(UUID.class))).thenReturn(Optional.of(customer));
        Mockito.when(vehicleRepository.existsByLicensePlate(Mockito.anyString())).thenReturn(false);
        Mockito.when(vehicleRepository.save(Mockito.any(Vehicle.class))).thenReturn(vehicle);

        Vehicle saved = vehicleService.save(customer.getId(), vehicle);

        Assertions.assertAll(
            () -> Assertions.assertEquals(saved.getLicensePlate(), vehicle.getLicensePlate()),
            () -> Assertions.assertEquals(saved.getYear(), vehicle.getYear()),
            () -> Assertions.assertEquals(vehicle.getCustomer(), saved.getCustomer())
        );

        Mockito.verify(customerRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verify(vehicleRepository, Mockito.times(1)).existsByLicensePlate(Mockito.anyString());
        Mockito.verify(vehicleRepository, Mockito.times(1)).save(Mockito.any(Vehicle.class));

        Mockito.verifyNoMoreInteractions(customerRepository);
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldThrowCustomerNotFoundException() {
        String errMsg = "Cliente de id '" + customer.getId() + "' não foi encontrado.";
        Mockito.when(customerRepository.findById(Mockito.any(UUID.class))).thenReturn(Optional.empty());

        CustomerNotFoundException ex = Assertions.assertThrows(
            CustomerNotFoundException.class,
            () -> vehicleService.save(customer.getId(), vehicle)
        );

        Assertions.assertNotNull(ex);
        Assertions.assertEquals(errMsg, ex.getMessage());
        Mockito.verifyNoInteractions(vehicleRepository);
    }

    @Test
    void shouldThrowLicensePlateAlreadyExistsException() {
        String errMsg = "Placa '" + vehicle.getLicensePlate() + "' já está cadastrada!";
        Mockito.when(customerRepository.findById(Mockito.any(UUID.class))).thenReturn(Optional.of(customer));
        Mockito.when(vehicleRepository.existsByLicensePlate(Mockito.anyString())).thenReturn(true);

        LicensePlateAlreadyExistsException ex = Assertions.assertThrows(
                LicensePlateAlreadyExistsException.class,
                () -> vehicleService.save(customer.getId(), vehicle)
        );

        Assertions.assertNotNull(ex);
        Assertions.assertEquals(errMsg, ex.getMessage());

        Mockito.verify(customerRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verify(vehicleRepository, Mockito.times(1)).existsByLicensePlate(Mockito.anyString());
        Mockito.verify(vehicleRepository, Mockito.never()).save(Mockito.any(Vehicle.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldThrowInvalidVehicleYearExceptionWhenYearIsToFarInPast() {
        String errMsg = "O ano do veículo deve estar entre 1880 e " + (Year.now().getValue() + 1);
        Mockito.when(customerRepository.findById(Mockito.any(UUID.class))).thenReturn(Optional.of(customer));
        Mockito.when(vehicleRepository.existsByLicensePlate(Mockito.anyString())).thenReturn(false);

        vehicle.setYear((short) 1000);
        InvalidVehicleYearException ex = Assertions.assertThrows(
                InvalidVehicleYearException.class,
                () -> vehicleService.save(customer.getId(), vehicle)
        );

        Assertions.assertNotNull(ex);
        Assertions.assertEquals(errMsg, ex.getMessage());

        Mockito.verify(customerRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verify(vehicleRepository, Mockito.times(1)).existsByLicensePlate(Mockito.anyString());
        Mockito.verify(vehicleRepository, Mockito.never()).save(Mockito.any(Vehicle.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldThrowInvalidVehicleYearExceptionWhenYearIsToFarInFuture() {
        String errMsg = "O ano do veículo deve estar entre 1880 e " + (Year.now().getValue() + 1);
        Mockito.when(customerRepository.findById(Mockito.any(UUID.class))).thenReturn(Optional.of(customer));
        Mockito.when(vehicleRepository.existsByLicensePlate(Mockito.anyString())).thenReturn(false);

        vehicle.setYear((short) (Year.now().getValue() + 2));
        InvalidVehicleYearException ex = Assertions.assertThrows(
                InvalidVehicleYearException.class,
                () -> vehicleService.save(customer.getId(), vehicle)
        );

        Assertions.assertNotNull(ex);
        Assertions.assertEquals(errMsg, ex.getMessage());

        Mockito.verify(customerRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verify(vehicleRepository, Mockito.times(1)).existsByLicensePlate(Mockito.anyString());
        Mockito.verify(vehicleRepository, Mockito.never()).save(Mockito.any(Vehicle.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldReturnVehicleById() {
        Mockito.when(vehicleRepository.findById(Mockito.any(UUID.class))).thenReturn(Optional.of(vehicle));

        Vehicle v = vehicleService.findById(vehicle.getId());
        Assertions.assertAll(
                () -> Assertions.assertEquals(v.getId(), vehicle.getId()),
                () -> Assertions.assertEquals(v.getCustomer(), vehicle.getCustomer())
        );

        Mockito.verify(vehicleRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldThrowVehicleNotFoundExceptionWhenFindingById() {
        String errMsg = "Veículo com id '" + vehicle.getId() + "' não foi encontrado.";
        Mockito.when(vehicleRepository.findById(Mockito.any(UUID.class))).thenThrow(new VehicleNotFoundException("Veículo com id '" + vehicle.getId() + "' não foi encontrado."));

        VehicleNotFoundException ex = Assertions.assertThrows(
                VehicleNotFoundException.class,
                () -> vehicleService.findById(vehicle.getId())
        );

        Assertions.assertAll(
                () -> Assertions.assertNotNull(ex),
                () -> Assertions.assertEquals(errMsg, ex.getMessage())
        );

        Mockito.verify(vehicleRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldReturnVehicleByLicensePlate() {
        Mockito.when(vehicleRepository.findByLicensePlate(Mockito.anyString())).thenReturn(Optional.of(vehicle));

        Vehicle v = vehicleService.findByLicensePlate(vehicle.getLicensePlate());
        Assertions.assertAll(
                () -> Assertions.assertEquals(v.getId(), vehicle.getId()),
                () -> Assertions.assertEquals(v.getCustomer(), vehicle.getCustomer())
        );

        Mockito.verify(vehicleRepository, Mockito.times(1)).findByLicensePlate(Mockito.anyString());
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }

    @Test
    void shouldThrowVehicleNotFoundExceptionWhenFindingByLicensePlate() {
        String errMsg = "Veículo com placa '" + vehicle.getLicensePlate() + "' não foi encontrado.";
        Mockito.when(vehicleRepository.findById(Mockito.any(UUID.class))).thenThrow(new VehicleNotFoundException(errMsg));

        VehicleNotFoundException ex = Assertions.assertThrows(
                VehicleNotFoundException.class,
                () -> vehicleService.findById(vehicle.getId())
        );

        Assertions.assertAll(
                () -> Assertions.assertNotNull(ex),
                () -> Assertions.assertEquals(errMsg, ex.getMessage())
        );

        Mockito.verify(vehicleRepository, Mockito.times(1)).findById(Mockito.any(UUID.class));
        Mockito.verifyNoMoreInteractions(vehicleRepository);
    }
}
