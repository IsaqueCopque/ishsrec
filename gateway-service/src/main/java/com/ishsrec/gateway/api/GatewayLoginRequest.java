package com.ishsrec.gateway.api;

public class GatewayLoginRequest {

    private String email;
    private String password;

    public GatewayLoginRequest() {
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}

