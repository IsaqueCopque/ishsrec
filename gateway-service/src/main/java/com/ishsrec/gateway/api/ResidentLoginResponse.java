package com.ishsrec.gateway.api;

import java.util.Map;

public class ResidentLoginResponse {

    private String token;
    private Map<String, Object> resident;

    public ResidentLoginResponse() {
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
}

