package com.uallace.fixflow_backend.modules.item.services;

import com.uallace.fixflow_backend.modules.item.entities.Item;
import com.uallace.fixflow_backend.modules.item.exceptions.*;
import com.uallace.fixflow_backend.modules.item.repositories.ItemRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ItemService {
    private final ItemRepository itemRepository;

    public Item save(Item item) {
        if(itemRepository.existsByName(item.getName())) throw new ItemNameAlreadyExistsException(item.getName());
        if(item.getQuantity() == null || 0 > item.getQuantity()) item.setQuantity(0);
        return itemRepository.save(item);
    }

    public Item findById(UUID id) {
        return itemRepository.findById(id).orElseThrow(() -> new ItemNotFoundException("Item de id '" + id.toString() + "' não encontrado!"));
    }

    public Item findByName(String name) {
        return itemRepository.findByName(name).orElseThrow(() -> new ItemNotFoundException("Item de nome '" + name + "' não encontrado!"));
    }

    @Transactional
    public Item update(String strId, Item item) {
        UUID id;

        try {
            id = UUID.fromString(strId);
        } catch (IllegalArgumentException ex) {
            throw new ItemInvalidIDException("Por favor, forneça um ID válido para o item!");
        }

        Item actual = itemRepository.findById(id).orElseThrow(() -> new ItemNotFoundException("Item de id '" + id.toString() + "' não encontrado!"));

        if(item.getName() != null) {
            if(itemRepository.existsByName(item.getName())) throw new ItemNameAlreadyExistsException(item.getName());
            actual.setName(item.getName());
        }

        if(item.getPrice() != null) {
            if(0 >= item.getPrice().compareTo(BigDecimal.ZERO)) throw new ItemInvalidPriceException("Preço do item não pode ser 0 ou menor!");
            actual.setPrice(item.getPrice());
        }

        if(item.getQuantity() != null) {
            if (0 > item.getQuantity()) throw new ItemInvalidQuantityException("Quantidade não pode ser menor que 0");
            actual.setQuantity(item.getQuantity());
        }

        return actual;
    }
}
