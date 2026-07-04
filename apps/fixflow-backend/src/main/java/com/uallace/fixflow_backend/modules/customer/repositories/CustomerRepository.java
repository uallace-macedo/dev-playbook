package com.uallace.fixflow_backend.modules.customer.repositories;

import com.uallace.fixflow_backend.modules.customer.entities.Customer;
import jakarta.annotation.Nonnull;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface CustomerRepository extends JpaRepository<Customer, UUID> {
    Optional<Customer> findByCpf(String cpf);
    Optional<Customer> findByEmail(String email);
}
