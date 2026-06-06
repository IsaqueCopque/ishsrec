package com.ishsrec.resident.controller;

import com.ishsrec.resident.model.Resident;
import com.ishsrec.resident.service.ResidentService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.net.URI;

@RestController
@RequestMapping("/residents")
public class ResidentController {

    private final ResidentService residentService;

    public ResidentController(ResidentService residentService) {
        this.residentService = residentService;
    }

    @PostMapping
    public ResponseEntity<?> createResident(@RequestBody Resident resident) {
        try {
            Resident created = residentService.createResident(resident);
            return ResponseEntity
                    .created(URI.create("/residents/" + created.getId()))
                    .body(created);
        } catch (IllegalArgumentException ex) {
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    @GetMapping("/{id}")
    @PreAuthorize("#id == authentication.principal")
    public ResponseEntity<Resident> getResident(@PathVariable Long id) {
        return residentService.getResident(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
}

