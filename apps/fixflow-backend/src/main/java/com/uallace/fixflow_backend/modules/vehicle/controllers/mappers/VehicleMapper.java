package com.uallace.fixflow_backend.modules.vehicle.controllers.mappers;

import com.uallace.fixflow_backend.modules.customer.controllers.mappers.CustomerMapper;
import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.CreateVehicleDTO;
import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.VehicleCompleteResponseDTO;
import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.VehicleResponseDTO;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(
        componentModel = "spring",
        uses = { CustomerMapper.class },
        unmappedSourcePolicy = ReportingPolicy.IGNORE
)
public interface VehicleMapper {
    VehicleMapper INSTANCE = Mappers.getMapper(VehicleMapper.class);

    VehicleResponseDTO toDTO(Vehicle vehicle);
    VehicleCompleteResponseDTO toCompleteDTO(Vehicle vehicle);

    Vehicle toEntity(CreateVehicleDTO dto);
}
