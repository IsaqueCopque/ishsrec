package com.ishsrec.resident.service;

import com.ishsrec.resident.model.Scene;
import com.ishsrec.resident.repository.SceneRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class SceneService {

    private final SceneRepository sceneRepository;

    public SceneService(SceneRepository sceneRepository) {
        this.sceneRepository = sceneRepository;
    }

    @Transactional
    public Scene createScene(Scene scene) {
        validateScene(scene);
        return sceneRepository.save(scene);
    }

    @Transactional
    public Optional<Scene> updateScene(Long id, Scene updated) {
        validateScene(updated);
        return sceneRepository.findById(id).map(existing -> {
            existing.setStartTime(updated.getStartTime());
            existing.setEndTime(updated.getEndTime());
            existing.setMonday(updated.isMonday());
            existing.setTuesday(updated.isTuesday());
            existing.setWednesday(updated.isWednesday());
            existing.setThursday(updated.isThursday());
            existing.setFriday(updated.isFriday());
            existing.setSaturday(updated.isSaturday());
            existing.setSunday(updated.isSunday());
            existing.setDevicesIds(updated.getDevicesIds());
            existing.setAuthor(updated.getAuthor());
            return sceneRepository.save(existing);
        });
    }

    public Optional<Scene> getScene(Long id) {
        return sceneRepository.findById(id);
    }

    private void validateScene(Scene scene) {
        if (scene == null) {
            throw new IllegalArgumentException("Scene must not be null");
        }

        if (scene.getStartTime() == null || scene.getEndTime() == null) {
            throw new IllegalArgumentException("Scene startTime and endTime must not be null");
        }

        if (scene.getStartTime() < 0 || scene.getStartTime() > 23
                || scene.getEndTime() < 0 || scene.getEndTime() > 23) {
            throw new IllegalArgumentException("Scene startTime and endTime must be between 0 and 23");
        }

        if (scene.getStartTime() >= scene.getEndTime()) {
            throw new IllegalArgumentException("Scene startTime must be before endTime");
        }

        if(scene.getAuthor() == null) {
            throw new IllegalArgumentException("Scene author must not be null");
        }

        if (scene.getDevicesIds() == null || scene.getDevicesIds().trim().isEmpty()) {
            throw new IllegalArgumentException("Scene devicesIds must not be empty");
        }
    }
}

