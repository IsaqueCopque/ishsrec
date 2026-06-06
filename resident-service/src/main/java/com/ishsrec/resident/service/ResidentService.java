package com.ishsrec.resident.service;

import com.ishsrec.resident.api.LoginResponse;
import com.ishsrec.resident.model.Resident;
import com.ishsrec.resident.repository.ResidentRepository;
import com.ishsrec.resident.security.JwtService;
import com.ishsrec.resident.messaging.ResidentEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Optional;

@Service
public class ResidentService {

    private final ResidentRepository residentRepository;
    private final ResidentEventPublisher eventPublisher;
    private final JwtService jwtService;

    public ResidentService(ResidentRepository residentRepository,
                           ResidentEventPublisher eventPublisher,
                           JwtService jwtService) {
        this.residentRepository = residentRepository;
        this.eventPublisher = eventPublisher;
        this.jwtService = jwtService;
    }

    @Transactional
    public Resident createResident(Resident resident) {
        validateResident(resident);
        resident.setPassword(hashPassword(resident.getPassword()));
        Resident saved = residentRepository.save(resident);
        eventPublisher.publishResidentCreated(saved);
        return saved;
    }

    public LoginResponse login(String email, String password) {
        if (email == null || email.trim().isEmpty()) {
            throw new IllegalArgumentException("Email must not be empty");
        }
        if (password == null || password.trim().isEmpty()) {
            throw new IllegalArgumentException("Password must not be empty");
        }

        Resident resident = residentRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalArgumentException("Invalid credentials"));

        String hashed = hashPassword(password);
        if (!hashed.equals(resident.getPassword())) {
            throw new IllegalArgumentException("Invalid credentials");
        }

        String token = jwtService.generateToken(resident);
        return new LoginResponse(token, resident);
    }

    private void validateResident(Resident resident) {
        if (resident == null) {
            throw new IllegalArgumentException("Resident must not be null");
        }

        if (resident.getName() == null || resident.getName().trim().isEmpty()) {
            throw new IllegalArgumentException("Resident name must not be empty");
        }

        if (resident.getPassword() == null || resident.getPassword().trim().isEmpty()) {
            throw new IllegalArgumentException("Resident password must not be empty");
        } else if (resident.getPassword().length() < 8) {
            throw new IllegalArgumentException("Resident password must be at least 8 characters long");
        }
        
        if (resident.getEmail() == null || resident.getEmail().trim().isEmpty()) {
            throw new IllegalArgumentException("Resident email must not be empty");
        }
    }

    private String hashPassword(String rawPassword) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(rawPassword.getBytes(StandardCharsets.UTF_8));
            StringBuilder hexString = new StringBuilder();
            for (byte b : hash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("Failed to hash password", e);
        }
    }

    public Optional<Resident> getResident(Long id) {
        return residentRepository.findById(id);
    }
}

