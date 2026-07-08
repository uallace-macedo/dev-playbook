package com.uallace.fixflow_backend.modules.item.services;

import com.uallace.fixflow_backend.modules.item.entities.Item;
import com.uallace.fixflow_backend.modules.item.exceptions.*;
import com.uallace.fixflow_backend.modules.item.repositories.ItemRepository;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;

@ExtendWith(MockitoExtension.class)
public class ItemServiceTest {

    @Mock
    private ItemRepository itemRepository;

    @InjectMocks
    private ItemService itemService;

    private Item item;
    private UUID itemId;

    @BeforeEach
    void setup() {
        itemId = UUID.fromString("3d9a2ff1-e2ca-499f-9fc6-926d83cf9fb3");
        item = Item.builder()
                .id(itemId)
                .name("Item Original")
                .price(new BigDecimal("10.00"))
                .quantity(5)
                .build();
    }

    @Nested
    @DisplayName("Testes do método save")
    class SaveTests {

        @Test
        @DisplayName("Deve salvar um item com sucesso quando os dados forem válidos")
        void shouldSaveItemSuccessfully() {
            Mockito.when(itemRepository.existsByName(item.getName())).thenReturn(false);
            Mockito.when(itemRepository.save(any(Item.class))).thenReturn(item);

            Item savedItem = itemService.save(item);

            Assertions.assertNotNull(savedItem);
            Assertions.assertEquals(5, savedItem.getQuantity());
            Mockito.verify(itemRepository, Mockito.times(1)).save(item);
        }

        @Test
        @DisplayName("Deve lançar ItemNameAlreadyExistsException quando o nome já existir")
        void shouldThrowExceptionWhenNameAlreadyExists() {
            Mockito.when(itemRepository.existsByName(item.getName())).thenReturn(true);

            Assertions.assertThrows(ItemNameAlreadyExistsException.class, () -> itemService.save(item));
            Mockito.verify(itemRepository, Mockito.never()).save(any(Item.class));
        }

        @Test
        @DisplayName("Deve definir a quantidade como 0 se ela for fornecida como nula")
        void shouldSetQuantityToZeroWhenQuantityIsNull() {
            item.setQuantity(null);
            Mockito.when(itemRepository.existsByName(item.getName())).thenReturn(false);
            Mockito.when(itemRepository.save(any(Item.class))).thenAnswer(invocation -> invocation.getArgument(0));

            Item savedItem = itemService.save(item);

            Assertions.assertEquals(0, savedItem.getQuantity());
        }

        @Test
        @DisplayName("Deve definir a quantidade como 0 se ela for menor que 0")
        void shouldSetQuantityToZeroWhenQuantityIsNegative() {
            item.setQuantity(-5);
            Mockito.when(itemRepository.existsByName(item.getName())).thenReturn(false);
            Mockito.when(itemRepository.save(any(Item.class))).thenAnswer(invocation -> invocation.getArgument(0));

            Item savedItem = itemService.save(item);

            Assertions.assertEquals(0, savedItem.getQuantity());
        }
    }

    @Nested
    @DisplayName("Testes do método findById")
    class FindByIdTests {

        @Test
        @DisplayName("Deve retornar o item por ID com sucesso")
        void shouldFindItemByIdSuccessfully() {
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));

            Item foundItem = itemService.findById(itemId);

            Assertions.assertEquals(item, foundItem);
        }

        @Test
        @DisplayName("Deve lançar ItemNotFoundException quando ID não existir")
        void shouldThrowNotFoundExceptionWhenIdDoesNotExist() {
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.empty());

            Assertions.assertThrows(ItemNotFoundException.class, () -> itemService.findById(itemId));
        }
    }

    @Nested
    @DisplayName("Testes do método findByName")
    class FindByNameTests {

        @Test
        @DisplayName("Deve retornar o item por nome com sucesso")
        void shouldFindItemByNameSuccessfully() {
            Mockito.when(itemRepository.findByName("Item Original")).thenReturn(Optional.of(item));

            Item foundItem = itemService.findByName("Item Original");

            Assertions.assertEquals(item, foundItem);
        }

        @Test
        @DisplayName("Deve lançar ItemNotFoundException quando nome não existir")
        void shouldThrowNotFoundExceptionWhenNameDoesNotExist() {
            Mockito.when(itemRepository.findByName("Inexistente")).thenReturn(Optional.empty());

            Assertions.assertThrows(ItemNotFoundException.class, () -> itemService.findByName("Inexistente"));
        }
    }

    @Nested
    @DisplayName("Testes do método update")
    class UpdateTests {

        private Item updateFields;

        @BeforeEach
        void setupUpdate() {
            updateFields = new Item();
        }

        @Test
        @DisplayName("Deve lançar ItemInvalidIDException quando string do ID for inválida")
        void shouldThrowInvalidIdExceptionWhenIdIsMalformed() {
            Assertions.assertThrows(ItemInvalidIDException.class, () -> itemService.update("id-invalido", updateFields));
        }

        @Test
        @DisplayName("Deve lançar ItemNotFoundException quando o item do update não for encontrado")
        void shouldThrowNotFoundExceptionDuringUpdate() {
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.empty());

            Assertions.assertThrows(ItemNotFoundException.class, () -> itemService.update(itemId.toString(), updateFields));
        }

        @Test
        @DisplayName("Deve atualizar o nome com sucesso se ele for alterado e for único")
        void shouldUpdateNameSuccessfully() {
            updateFields.setName("Novo Nome");
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));
            Mockito.when(itemRepository.existsByName("Novo Nome")).thenReturn(false);

            Item updated = itemService.update(itemId.toString(), updateFields);

            Assertions.assertEquals("Novo Nome", updated.getName());
        }

        @Test
        @DisplayName("Deve lançar ItemNameAlreadyExistsException se o novo nome já existir")
        void shouldThrowExceptionWhenUpdatedNameExists() {
            updateFields.setName("Nome Duplicado");
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));
            Mockito.when(itemRepository.existsByName("Nome Duplicado")).thenReturn(true);

            Assertions.assertThrows(ItemNameAlreadyExistsException.class, () -> itemService.update(itemId.toString(), updateFields));
        }

        @Test
        @DisplayName("Deve atualizar o preço com sucesso")
        void shouldUpdatePriceSuccessfully() {
            updateFields.setPrice(new BigDecimal("25.50"));
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));

            Item updated = itemService.update(itemId.toString(), updateFields);

            Assertions.assertEquals(new BigDecimal("25.50"), updated.getPrice());
        }

        @Test
        @DisplayName("Deve lançar ItemInvalidPriceException se o preço atualizado for zero ou menor")
        void shouldThrowInvalidPriceExceptionWhenPriceIsZeroOrNegative() {
            updateFields.setPrice(BigDecimal.ZERO);
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));

            Assertions.assertThrows(ItemInvalidPriceException.class, () -> itemService.update(itemId.toString(), updateFields));
        }

        @Test
        @DisplayName("Deve atualizar a quantidade com sucesso")
        void shouldUpdateQuantitySuccessfully() {
            updateFields.setQuantity(20);
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));

            Item updated = itemService.update(itemId.toString(), updateFields);

            Assertions.assertEquals(20, updated.getQuantity());
        }

        @Test
        @DisplayName("Deve lançar ItemInvalidQuantityException se a quantidade for menor que zero")
        void shouldThrowInvalidQuantityExceptionWhenQuantityIsNegative() {
            updateFields.setQuantity(-1);
            Mockito.when(itemRepository.findById(itemId)).thenReturn(Optional.of(item));

            Assertions.assertThrows(ItemInvalidQuantityException.class, () -> itemService.update(itemId.toString(), updateFields));
        }
    }
}