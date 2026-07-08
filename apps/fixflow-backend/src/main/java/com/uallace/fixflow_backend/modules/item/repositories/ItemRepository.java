package com.uallace.fixflow_backend.modules.item.repositories;

import com.uallace.fixflow_backend.modules.item.entities.Item;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface ItemRepository extends JpaRepository<Item, UUID> {
    boolean existsByName(String name);
    Optional<Item> findByName(String name);
}
