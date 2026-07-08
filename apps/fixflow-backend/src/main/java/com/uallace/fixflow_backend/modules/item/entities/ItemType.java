package com.uallace.fixflow_backend.modules.item.entities;

import lombok.Getter;

@Getter
public enum ItemType {
    PART("PART"),
    SERVICE("SERVICE");

    private final String label;

    ItemType(String label) {
        this.label = label;
    }
}
