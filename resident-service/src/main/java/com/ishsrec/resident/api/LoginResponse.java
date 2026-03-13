package com.ishsrec.resident.api;

import com.ishsrec.resident.model.Resident;

public class LoginResponse {

    private String token;
    private Resident resident;

    public LoginResponse() {
    }

    public LoginResponse(String token, Resident resident) {
        this.token = token;
        this.resident = resident;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public Resident getResident() {
        return resident;
    }

    public void setResident(Resident resident) {
        this.resident = resident;
    }
}

