package com.uallace.fixflow_backend.modules.item.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.uallace.fixflow_backend.modules.item.controllers.dto.*;
import com.uallace.fixflow_backend.modules.item.controllers.mappers.ItemMapper;
import com.uallace.fixflow_backend.modules.item.entities.Item;
import com.uallace.fixflow_backend.modules.item.services.ItemService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;

@WebMvcTest(ItemController.class)
public class ItemControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private ItemService itemService;

    @MockitoBean
    private ItemMapper itemMapper;

    private Item item;
    private ItemResponseDTO itemResponseDTO;
    private UUID itemId;

    @BeforeEach
    void setup() {
        itemId = UUID.fromString("3d9a2ff1-e2ca-499f-9fc6-926d83cf9fb3");
        OffsetDateTime now = OffsetDateTime.now();

        item = Item.builder()
            .id(itemId)
            .name("Item Teste")
            .price(new BigDecimal("100.00"))
            .quantity(10)
            .createdAt(now)
            .build();

        itemResponseDTO = ItemResponseDTOFixture.build(itemId, "Item Teste", new BigDecimal("100.00"), 10, now);
    }

    @Nested
    @DisplayName("Testes do endpoint GET /api/v1/items/{identifier}")
    class FindTests {

        @Test
        @DisplayName("Deve buscar por ID com sucesso quando o identificador for um UUID válido")
        void shouldFindByIdSuccessfully() throws Exception {
            Mockito.when(itemService.findById(itemId)).thenReturn(item);
            Mockito.when(itemMapper.toDTO(item)).thenReturn(itemResponseDTO);

            mockMvc.perform(MockMvcRequestBuilders.get("/api/v1/items/" + itemId)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.jsonPath("$.id").value(itemId.toString()))
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("Item Teste"));

            Mockito.verify(itemService, Mockito.times(1)).findById(itemId);
            Mockito.verify(itemService, Mockito.never()).findByName(any());
        }

        @Test
        @DisplayName("Deve buscar por Nome através do catch quando o identificador não for um UUID")
        void shouldFindByNameWhenIdentifierIsNotUUID() throws Exception {
            String nameIdentifier = "Item-Qualquer";
            Mockito.when(itemService.findByName(nameIdentifier)).thenReturn(item);
            Mockito.when(itemMapper.toDTO(item)).thenReturn(itemResponseDTO);

            mockMvc.perform(MockMvcRequestBuilders.get("/api/v1/items/" + nameIdentifier)
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.jsonPath("$.name").value("Item Teste"));

            Mockito.verify(itemService, Mockito.times(1)).findByName(nameIdentifier);
            Mockito.verify(itemService, Mockito.never()).findById(any());
        }
    }

    @Nested
    @DisplayName("Testes do endpoint POST /api/v1/items")
    class SaveTests {

        @Test
        @DisplayName("Deve salvar um item com sucesso quando o DTO for válido")
        void shouldSaveItemSuccessfully() throws Exception {
            CreateItemDTO createDTO = CreateItemDTOFixture.build("Item Teste", new BigDecimal("100.00"), 10);

            Mockito.when(itemMapper.toEntity(any(CreateItemDTO.class))).thenReturn(item);
            Mockito.when(itemService.save(any(Item.class))).thenReturn(item);
            Mockito.when(itemMapper.toDTO(item)).thenReturn(itemResponseDTO);

            mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/items")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(createDTO)))
                .andExpect(MockMvcResultMatchers.status().isCreated())
                .andExpect(MockMvcResultMatchers.jsonPath("$.id").value(itemId.toString()));
        }

        @Test
        @DisplayName("Deve retornar 400 Bad Request quando falhar nas validações do @Valid")
        void shouldReturnBadRequestWhenDTOIsInvalid() throws Exception {
            // Nome inválido (menos de 2 caracteres) para quebrar o @Valid do record
            CreateItemDTO invalidDTO = CreateItemDTOFixture.build("A", new BigDecimal("100.00"), 10);

            mockMvc.perform(MockMvcRequestBuilders.post("/api/v1/items")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidDTO)))
                .andExpect(MockMvcResultMatchers.status().isBadRequest());

            Mockito.verifyNoInteractions(itemService);
        }
    }

    @Nested
    @DisplayName("Testes do endpoint PUT /api/v1/items/{id}")
    class UpdateTests {

        @Test
        @DisplayName("Deve atualizar o item com sucesso quando houver pelo menos um campo preenchido")
        void shouldUpdateItemSuccessfully() throws Exception {
            UpdateItemDTO updateDTO = UpdateItemDTOFixture.build("Nome Atualizado", null, null);

            Mockito.when(itemMapper.toEntity(any(UpdateItemDTO.class))).thenReturn(item);
            Mockito.when(itemService.update(eq(itemId.toString()), any(Item.class))).thenReturn(item);
            Mockito.when(itemMapper.toDTO(item)).thenReturn(itemResponseDTO);

            mockMvc.perform(MockMvcRequestBuilders.put("/api/v1/items/" + itemId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateDTO)))
                .andExpect(MockMvcResultMatchers.status().isOk());
        }

        @Test
        @DisplayName("Deve retornar 204 No Content se todos os campos do UpdateItemDTO forem nulos")
        void shouldReturnNoContentWhenAllFieldsAreNull() throws Exception {
            UpdateItemDTO emptyUpdateDTO = UpdateItemDTOFixture.build(null, null, null);

            mockMvc.perform(MockMvcRequestBuilders.put("/api/v1/items/" + itemId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(emptyUpdateDTO)))
                .andExpect(MockMvcResultMatchers.status().isNoContent())
                .andExpect(MockMvcResultMatchers.jsonPath("$").doesNotExist());

            Mockito.verifyNoInteractions(itemMapper);
            Mockito.verifyNoInteractions(itemService);
        }
    }
}