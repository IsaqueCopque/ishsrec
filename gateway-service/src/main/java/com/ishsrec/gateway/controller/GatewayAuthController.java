package com.ishsrec.gateway.controller;

import com.ishsrec.gateway.api.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class GatewayAuthController {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String residentServiceBaseUrl;
    private final String messagesServiceBaseUrl;

    public GatewayAuthController(
            @Value("${services.resident.base-url:http://localhost:8080}") String residentServiceBaseUrl,
            @Value("${services.messages.base-url:http://localhost:5000}") String messagesServiceBaseUrl
    ) {
        this.residentServiceBaseUrl = residentServiceBaseUrl;
        this.messagesServiceBaseUrl = messagesServiceBaseUrl;
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

        ResidentLoginResponse residentLogin = authResponse.getBody();
        Map<String, Object> resident = residentLogin.getResident();
        Object residentIdObj = resident != null ? resident.get("id") : null;
        String residentId = residentIdObj != null ? String.valueOf(residentIdObj) : null;

        // Call messages-service /api/devices?residentId=...
        // String devicesUrl = UriComponentsBuilder
        //         .fromHttpUrl(messagesServiceBaseUrl + "/api/devices")
        //         .queryParam("residentId", residentId)
        //         .toUriString();

        // ResponseEntity<DevicesResponse> devicesResponse =
        //         restTemplate.getForEntity(devicesUrl, DevicesResponse.class);

        // List<Map<String, Object>> devices =
        //         devicesResponse.getBody() != null ? devicesResponse.getBody().getDevices() : List.of();

        // GatewayLoginResponse gatewayResponse =
        //         new GatewayLoginResponse(residentLogin.getToken(), resident, devices);

        GatewayLoginResponse gatewayResponse = new GatewayLoginResponse(residentLogin.getToken(), resident, List.of());

        return ResponseEntity.ok(gatewayResponse);
    }
}

