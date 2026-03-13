package com.ishsrec.resident.repository;

import com.ishsrec.resident.model.Resident;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ResidentRepository extends JpaRepository<Resident, Long> {

    Optional<Resident> findByEmail(String email);
}

