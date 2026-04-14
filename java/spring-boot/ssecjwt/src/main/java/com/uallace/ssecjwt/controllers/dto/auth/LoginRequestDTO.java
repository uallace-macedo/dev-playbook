package com.uallace.ssecjwt.controllers.dto.auth;

public record LoginRequestDTO(
        String email,
        String password
) {}
