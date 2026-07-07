package com.uallace.fixflow_backend.modules.vehicle.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTO;
import com.uallace.fixflow_backend.modules.customer.controllers.dto.CustomerResponseDTOFixture;
import com.uallace.fixflow_backend.modules.vehicle.controllers.dto.*;
import com.uallace.fixflow_backend.modules.vehicle.controllers.mappers.VehicleMapper;
import com.uallace.fixflow_backend.modules.vehicle.entities.Vehicle;
import com.uallace.fixflow_backend.modules.vehicle.exceptions.VehicleNotFoundException;
import com.uallace.fixflow_backend.modules.vehicle.services.VehicleService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(VehicleController.class)
public class VehicleControllerTest {
    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    VehicleService vehicleService;

    @MockitoBean
    VehicleMapper vehicleMapper;

    @Autowired
    ObjectMapper objectMapper;

    String url;

    @BeforeEach
    void setup() {
        url = "/api/v1/vehicles";
    }

    @DisplayName("Create vehicle endpoint")
    @Nested
    class CreateVehicle {
        UUID customerId = UUID.randomUUID();
        CustomerResponseDTO customerResponseDTO = CustomerResponseDTOFixture.build(customerId, "customer", "customer@email.com", "(00) 00000-0000", "000.000.000-00");
        CreateVehicleDTO dto = CreateVehicleDTOFixture.build(customerId, "AAA0000", "XX", "XXXX", (short) 2010);

        UUID vehicleId = UUID.randomUUID();
        Vehicle vehicle = Vehicle.builder().licensePlate("AAA0000").build();
        Vehicle fakeSavedVehicle = Vehicle.builder().id(vehicleId).licensePlate("AAA0000").build();

        VehicleCompleteResponseDTO responseDTO = VehicleCompleteResponseDTOFixture.build(vehicleId, customerResponseDTO, "AAA0000", "XX", "XXXX", (short) 2010, OffsetDateTime.now());

        @Test
        @DisplayName("/POST - createVehicle")
        void shouldCreateVehicleSuccessfully() throws Exception {
            Mockito.when(vehicleMapper.toEntity(dto)).thenReturn(vehicle);
            Mockito.when(vehicleService.save(customerId, vehicle)).thenReturn(fakeSavedVehicle);
            Mockito.when(vehicleMapper.toCompleteDTO(fakeSavedVehicle)).thenReturn(responseDTO);

            mockMvc.perform(post(url)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(dto)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.id").value(vehicleId.toString()));
        }

        @Test
        @DisplayName("/POST - should return 400 Bad Request when validation fails")
        void shouldReturnBadRequestWhenDtoIsInvalid() throws Exception {
            mockMvc.perform(post(url)
                            .contentType(MediaType.APPLICATION_JSON)
                            .content("{}"))
                    .andExpect(status().isBadRequest());
        }
    }

    @DisplayName("Find by id endpoint")
    @Nested
    class FindById {
        UUID customerId = UUID.randomUUID();
        CustomerResponseDTO customerResponseDTO = CustomerResponseDTOFixture.build(customerId, "customer", "customer@email.com", "(00) 00000-0000", "000.000.000-00");
        UUID vehicleId = UUID.randomUUID();
        String licensePlate = "BBB1111";

        Vehicle vehicle = Vehicle.builder().id(vehicleId).licensePlate(licensePlate).build();
        VehicleCompleteResponseDTO responseDTO = VehicleCompleteResponseDTOFixture.build(vehicleId, customerResponseDTO, licensePlate, "XX", "XXXX", (short) 2015, OffsetDateTime.now());

        @Test
        @DisplayName("/GET /{id} - should find vehicle when ID is a valid UUID")
        void shouldFindVehicleByUuid() throws Exception {
            Mockito.when(vehicleService.findById(vehicleId)).thenReturn(vehicle);
            Mockito.when(vehicleMapper.toCompleteDTO(vehicle)).thenReturn(responseDTO);

            mockMvc.perform(get(url + "/" + vehicleId))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id").value(vehicleId.toString()))
                    .andExpect(jsonPath("$.licensePlate").value(licensePlate));
        }

        @Test
        @DisplayName("/GET /{id} - should find vehicle by license plate when ID is not a valid UUID")
        void shouldFindVehicleByLicensePlate() throws Exception {
            Mockito.when(vehicleService.findByLicensePlate(licensePlate)).thenReturn(vehicle);
            Mockito.when(vehicleMapper.toCompleteDTO(vehicle)).thenReturn(responseDTO);

            mockMvc.perform(get(url + "/" + licensePlate))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.id").value(vehicleId.toString()))
                    .andExpect(jsonPath("$.licensePlate").value(licensePlate));
        }

        @Test
        @DisplayName("/GET /{id} - should return 404 when vehicle is not found by UUID")
        void shouldReturnNotFoundWhenVehicleIdDoesNotExist() throws Exception {
            Mockito.when(vehicleService.findById(vehicleId))
                    .thenThrow(new VehicleNotFoundException("Vehicle not found"));

            mockMvc.perform(get(url + "/" + vehicleId))
                    .andExpect(status().isNotFound());
        }

        @Test
        @DisplayName("/GET /{id} - should return 404 when vehicle is not found by license plate")
        void shouldReturnNotFoundWhenLicensePlateDoesNotExist() throws Exception {
            Mockito.when(vehicleService.findByLicensePlate(licensePlate))
                    .thenThrow(new VehicleNotFoundException("Vehicle not found"));

            mockMvc.perform(get(url + "/" + licensePlate))
                    .andExpect(status().isNotFound());
        }
    }

    @DisplayName("Find all endpoint")
    @Nested
    class FindAll {
        @Test
        @DisplayName("/GET - should return a paged list of vehicles")
        void shouldReturnPagedVehicles() throws Exception {
            Pageable pageable = PageRequest.of(0, 20);

            Vehicle vehicle1 = Vehicle.builder().id(UUID.randomUUID()).licensePlate("AAA1111").build();
            List<Vehicle> vehicleList = List.of(vehicle1);
            Page<Vehicle> vehiclePage = new PageImpl<>(vehicleList, pageable, vehicleList.size());

            CustomerResponseDTO customerResponseDTO = CustomerResponseDTOFixture.build(UUID.randomUUID(), "customer", "customer@email.com", "(00) 00000-0000", "000.000.000-00");
            VehicleCompleteResponseDTO responseDTO = VehicleCompleteResponseDTOFixture.build(vehicle1.getId(), customerResponseDTO, "AAA1111", "XX", "XXXX", (short) 2010, OffsetDateTime.now());

            Mockito.when(vehicleService.findAll(pageable)).thenReturn(vehiclePage);
            Mockito.when(vehicleMapper.toCompleteDTO(vehicle1)).thenReturn(responseDTO);

            mockMvc.perform(get(url)
                            .param("page", "0")
                            .param("size", "20"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.content").isArray())
                    .andExpect(jsonPath("$.content[0].id").value(vehicle1.getId().toString()))
                    .andExpect(jsonPath("$.content[0].licensePlate").value("AAA1111"));
        }
    }
}