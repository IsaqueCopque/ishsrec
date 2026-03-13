package com.ishsrec.resident.controller;

import com.ishsrec.resident.api.LoginRequest;
import com.ishsrec.resident.api.LoginResponse;
import com.ishsrec.resident.service.ResidentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final ResidentService residentService;

    public AuthController(ResidentService residentService) {
        this.residentService = residentService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        try {
            LoginResponse response = residentService.login(request.getEmail(), request.getPassword());
            return ResponseEntity.ok(response);
        } catch (IllegalArgumentException ex) {
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
}

