package com.ishsrec.gateway.controller;

import com.ishsrec.gateway.api.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.List;
import java.util.Map;
import java.util.Objects;

@RestController
@RequestMapping("/api")
public class GatewayAuthController {

    private static final Logger log = LoggerFactory.getLogger(GatewayAuthController.class);

    private final RestTemplate restTemplate;
    private final String residentServiceBaseUrl;
    private final String messagesServiceBaseUrl;

    public GatewayAuthController(
            RestTemplate restTemplate,
            @Value("${services.resident.base-url:http://localhost:8080}") String residentServiceBaseUrl,
            @Value("${services.messages.base-url:http://localhost:5000}") String messagesServiceBaseUrl
    ) {
        this.residentServiceBaseUrl = residentServiceBaseUrl;
        this.messagesServiceBaseUrl = messagesServiceBaseUrl;
        this.restTemplate = restTemplate;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody GatewayLoginRequest request) {
        // Call resident-service /auth/login
        String authUrl = residentServiceBaseUrl + "/auth/login";
        ResponseEntity<ResidentLoginResponse> authResponse =
                restTemplate.postForEntity(authUrl, request, ResidentLoginResponse.class);

        if (!authResponse.getStatusCode().is2xxSuccessful() || authResponse.getBody() == null) {
            return ResponseEntity.status(authResponse.getStatusCode()).body(authResponse.getBody());
        }

        ResidentLoginResponse residentLogin = Objects.requireNonNull(authResponse.getBody());
        Map<String, Object> resident = residentLogin.getResident();
        Object residentIdObj = resident != null ? resident.get("id") : null;
        String residentId = residentIdObj != null ? String.valueOf(residentIdObj) : null;

        List<Map<String, Object>> devices = List.of();
        if (residentId != null) {
            String devicesUrl = UriComponentsBuilder
                    .fromHttpUrl(messagesServiceBaseUrl + "/api/devices")
                    .toUriString();
            try {
                ResponseEntity<DevicesResponse> devicesResponse =
                        restTemplate.getForEntity(devicesUrl, DevicesResponse.class);
                DevicesResponse devicesBody = devicesResponse.getBody();
                devices =
                        devicesBody != null && devicesBody.getDevices() != null
                                ? devicesBody.getDevices()
                                : List.of();
            } catch (RestClientException ex) {
                log.warn("Failed to load devices for resident {}: {}", residentId, ex.getMessage());
            }
        }

        GatewayLoginResponse gatewayResponse =
                new GatewayLoginResponse(residentLogin.getToken(), resident, devices);

        return ResponseEntity.ok(gatewayResponse);
    }
}

