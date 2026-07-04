package com.uallace.fixflow_backend.modules.customer.controllers.mappers;

import com.uallace.fixflow_backend.modules.customer.controllers.dto.CreateCustomerRequestDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(componentModel = "spring")
public interface CustomerMapper {
    CustomerMapper INSTANCE = Mappers.getMapper(CustomerMapper.class);

    CustomerResponseDTO toDTO(Customer customer);

    Customer toEntity(CreateCustomerRequestDTO customerData);
}
