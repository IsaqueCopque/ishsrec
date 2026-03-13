package com.ishsrec.resident.controller;

import com.ishsrec.resident.model.Scene;
import com.ishsrec.resident.service.SceneService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;

@RestController
@RequestMapping("/scenes")
public class SceneController {

    private final SceneService sceneService;

    public SceneController(SceneService sceneService) {
        this.sceneService = sceneService;
    }

    @PostMapping
    public ResponseEntity<?> createScene(@RequestBody Scene scene) {
        try {
            Scene created = sceneService.createScene(scene);
            return ResponseEntity
                    .created(URI.create("/scenes/" + created.getId()))
                    .body(created);
        } catch (IllegalArgumentException ex) {
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateScene(@PathVariable Long id, @RequestBody Scene scene) {
        try {
            return sceneService.updateScene(id, scene) 
                    .map(ResponseEntity::ok)
                    .orElseGet(() -> ResponseEntity.notFound().build());
        } catch (IllegalArgumentException ex) {
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Scene> getScene(@PathVariable Long id) {
        return sceneService.getScene(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
}

