package com.uallace.fixflow_backend.modules.item.controllers;

import com.uallace.fixflow_backend.modules.item.controllers.dto.CreateItemDTO;
import com.uallace.fixflow_backend.modules.item.controllers.dto.ItemResponseDTO;
import com.uallace.fixflow_backend.modules.item.controllers.dto.UpdateItemDTO;
import com.uallace.fixflow_backend.modules.item.controllers.mappers.ItemMapper;
import com.uallace.fixflow_backend.modules.item.entities.Item;
import com.uallace.fixflow_backend.modules.item.services.ItemService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/items")
public class ItemController {
    private final ItemService itemService;
    private final ItemMapper itemMapper;

    @GetMapping("/{identifier}")
    public ResponseEntity<ItemResponseDTO> find(@PathVariable("identifier") String identifier) {
        ItemResponseDTO itemDTO;

        try {
            UUID id = UUID.fromString(identifier);
            itemDTO = itemMapper.toDTO(itemService.findById(id));
        } catch (IllegalArgumentException ex) {
            itemDTO = itemMapper.toDTO(itemService.findByName(identifier));
        }

        return ResponseEntity.status(HttpStatus.OK).body(itemDTO);
    }

    @PostMapping("")
    public ResponseEntity<ItemResponseDTO> save(@Valid @RequestBody CreateItemDTO itemData) {
        Item item = itemMapper.toEntity(itemData);

        return ResponseEntity.status(HttpStatus.CREATED).body(
            itemMapper.toDTO(itemService.save(item))
        );
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> update(@PathVariable("id") String id, @RequestBody UpdateItemDTO itemDTO) {
        if(itemDTO.name() == null && itemDTO.price() == null && itemDTO.quantity() == null) return ResponseEntity.status(HttpStatus.NO_CONTENT).build();

        Item item = itemMapper.toEntity(itemDTO);
        return ResponseEntity.status(HttpStatus.OK).body(
            itemMapper.toDTO(itemService.update(id, item))
        );
    }
}
