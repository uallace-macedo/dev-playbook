package com.uallace.fixflow_backend.modules.item.controllers.mappers;

import com.uallace.fixflow_backend.modules.item.controllers.dto.*;
import com.uallace.fixflow_backend.modules.item.entities.Item;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mapstruct.factory.Mappers;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@ExtendWith(MockitoExtension.class)
public class ItemMapperTest {

    @InjectMocks
    private ItemMapper itemMapper = Mappers.getMapper(ItemMapper.class);

    private Item item;
    private ItemResponseDTO itemResponseDTO;
    private CreateItemDTO createItemDTO;
    private UpdateItemDTO updateItemDTO;

    @BeforeEach
    void setup() {
        UUID itemId = UUID.fromString("3d9a2ff1-e2ca-499f-9fc6-926d83cf9fb3");
        OffsetDateTime now = OffsetDateTime.now();

        item = Item.builder()
            .id(itemId)
            .name("Item de Teste")
            .price(new BigDecimal("50.00"))
            .quantity(5)
            .createdAt(now)
            .build();

        itemResponseDTO = ItemResponseDTOFixture.build(itemId, "Item de Teste", new BigDecimal("50.00"), 5, now);
        createItemDTO = CreateItemDTOFixture.build("Item de Teste", new BigDecimal("50.00"), 5);
        updateItemDTO = UpdateItemDTOFixture.build("Item de Teste", new BigDecimal("50.00"), 5);
    }

    @Test
    void shouldConvertToDTOSuccessfully() {
        ItemResponseDTO actualDTO = itemMapper.toDTO(item);

        Assertions.assertEquals(itemResponseDTO, actualDTO);
    }

    @Test
    void shouldConvertCreateDTOToEntitySuccessfully() {
        Item actualEntity = itemMapper.toEntity(createItemDTO);

        Assertions.assertAll(
            () -> Assertions.assertNull(actualEntity.getId()),
            () -> Assertions.assertEquals(createItemDTO.name(), actualEntity.getName()),
            () -> Assertions.assertEquals(createItemDTO.price(), actualEntity.getPrice()),
            () -> Assertions.assertEquals(createItemDTO.quantity(), actualEntity.getQuantity())
        );
    }

    @Test
    void shouldConvertUpdateDTOToEntitySuccessfully() {
        Item actualEntity = itemMapper.toEntity(updateItemDTO);

        Assertions.assertAll(
            () -> Assertions.assertNull(actualEntity.getId()),
            () -> Assertions.assertEquals(updateItemDTO.name(), actualEntity.getName()),
            () -> Assertions.assertEquals(updateItemDTO.price(), actualEntity.getPrice()),
            () -> Assertions.assertEquals(updateItemDTO.quantity(), actualEntity.getQuantity())
        );
    }
}