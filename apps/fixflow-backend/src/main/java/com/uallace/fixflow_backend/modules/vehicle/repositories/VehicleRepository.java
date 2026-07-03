package com.uallace.fixflow_backend.modules.vehicle.repositories;

import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface VehicleRepository extends JpaRepository<Vehicle, UUID> {}
