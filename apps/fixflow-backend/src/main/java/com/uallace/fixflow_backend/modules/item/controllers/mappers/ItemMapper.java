package com.uallace.fixflow_backend.modules.item.controllers.mappers;

import com.uallace.fixflow_backend.modules.item.controllers.dto.CreateItemDTO;
import com.uallace.fixflow_backend.modules.item.controllers.dto.ItemResponseDTO;
import com.uallace.fixflow_backend.modules.item.controllers.dto.UpdateItemDTO;
import com.uallace.fixflow_backend.modules.item.entities.Item;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper(componentModel = "spring")
public interface ItemMapper {
    ItemMapper INSTANCE = Mappers.getMapper(ItemMapper.class);

    ItemResponseDTO toDTO(Item item);

    Item toEntity(CreateItemDTO itemDTO);
    Item toEntity(UpdateItemDTO itemDTO);
}
