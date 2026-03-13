package com.ishsrec.gateway.api;

import java.util.List;
import java.util.Map;

public class GatewayLoginResponse {

    private String token;
    private Map<String, Object> resident;
    private List<Map<String, Object>> devices;

    public GatewayLoginResponse() {
    }

    public GatewayLoginResponse(String token, Map<String, Object> resident, List<Map<String, Object>> devices) {
        this.token = token;
        this.resident = resident;
        this.devices = devices;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public Map<String, Object> getResident() {
        return resident;
    }

    public void setResident(Map<String, Object> resident) {
        this.resident = resident;
    }

    public List<Map<String, Object>> getDevices() {
        return devices;
    }

    public void setDevices(List<Map<String, Object>> devices) {
        this.devices = devices;
    }
}

