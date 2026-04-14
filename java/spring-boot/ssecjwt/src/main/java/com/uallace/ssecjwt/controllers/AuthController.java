package com.uallace.ssecjwt.controllers;

import com.uallace.ssecjwt.controllers.dto.auth.LoginRequestDTO;
import com.uallace.ssecjwt.controllers.dto.auth.LoginResponseDTO;
import com.uallace.ssecjwt.controllers.dto.auth.RegisterRequestDTO;
import com.uallace.ssecjwt.controllers.dto.auth.RegisterResponseDTO;
import com.uallace.ssecjwt.domain.user.User;
import com.uallace.ssecjwt.infra.security.TokenService;
import com.uallace.ssecjwt.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final TokenService tokenService;

    @PostMapping("/login")
    public ResponseEntity login(@RequestBody LoginRequestDTO body) {
        User user = this.userRepository.findByEmail(body.email()).orElseThrow(() -> new RuntimeException("User not found exception"));
        if(passwordEncoder.matches(body.password(), user.getPassword())) {
            String token = this.tokenService.generateToken(user);
            return ResponseEntity.ok(new LoginResponseDTO(user.getName(), token));
        }

        return ResponseEntity.badRequest().build();
    }

    @PostMapping("/register")
    public ResponseEntity register(@RequestBody RegisterRequestDTO body) {
        Optional<User> user = this.userRepository.findByEmail(body.email());
        if(user.isPresent()) {
            return ResponseEntity.badRequest().build();
        }

        User newUser = new User();
        newUser.setName(body.name());
        newUser.setEmail(body.email());
        newUser.setPassword(passwordEncoder.encode(body.password()));

        this.userRepository.save(newUser);
        String token = this.tokenService.generateToken(newUser);
        return ResponseEntity.ok(new RegisterResponseDTO(newUser.getName(), token));
    }
}
