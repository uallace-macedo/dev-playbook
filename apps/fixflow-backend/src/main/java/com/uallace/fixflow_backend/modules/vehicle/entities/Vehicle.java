package com.uallace.fixflow_backend.modules.vehicle.entities;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.OffsetDateTime;
import java.util.UUID;

@Table(name = "tb_vehicle")
@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Vehicle {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @Column(name = "license_plate", length = 15, nullable = false, unique = true)
    private String licensePlate;

    @Column(length = 50, nullable = false)
    private String make;

    @Column(length = 50, nullable = false)
    private String model;

    @Column(nullable = false)
    private short year;

    @Column(name = "created_at", nullable = false, updatable = false)
    @CreationTimestamp
    private OffsetDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    @UpdateTimestamp
    private OffsetDateTime updatedAt;
}
