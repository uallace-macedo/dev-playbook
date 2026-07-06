package com.uallace.fixflow_backend.modules.vehicle.controllers;

import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.CreateVehicleDTO;
import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.VehicleCompleteResponseDTO;
import com.uallace.fixflow_backend.modules.vehicle.controllers.mappers.VehicleMapper;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import com.uallace.fixflow_backend.modules.vehicle.services.VehicleService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/vehicles")
public class VehicleController {
    private final VehicleService vehicleService;
    private final VehicleMapper vehicleMapper;

    @PostMapping("")
    public ResponseEntity<VehicleCompleteResponseDTO> createVehicle(@Valid @RequestBody CreateVehicleDTO vehicleData) {
        Vehicle vehicle = vehicleMapper.toEntity(vehicleData);

        VehicleCompleteResponseDTO savedVehicle = vehicleMapper.toCompleteDTO(
            vehicleService.save(vehicleData.customerId(), vehicle)
        );

        return ResponseEntity.status(HttpStatus.CREATED).body(savedVehicle);
    }

    @GetMapping("/{id}")
    public ResponseEntity<VehicleCompleteResponseDTO> findById(@PathVariable("id") String id) {
        Vehicle vehicle;

        try {
            UUID uuid = UUID.fromString(id);
            vehicle = vehicleService.findById(uuid);
        } catch (IllegalArgumentException e) {
            vehicle = vehicleService.findByLicensePlate(id);
        }

        return ResponseEntity.status(HttpStatus.OK).body(
            vehicleMapper.toCompleteDTO(vehicle)
        );
    }

    @GetMapping("")
    public ResponseEntity<Page<VehicleCompleteResponseDTO>> findAll(@PageableDefault(page = 0, size = 20) Pageable pageable) {
        return ResponseEntity.status(HttpStatus.OK).body(
                vehicleService.findAll(pageable).map(vehicleMapper::toCompleteDTO)
        );
    }
}
