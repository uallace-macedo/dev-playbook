package com.uallace.ssecjwt.controllers.dto.auth;

public record RegisterRequestDTO(
        String name,
        String email,
        String password
) {}
