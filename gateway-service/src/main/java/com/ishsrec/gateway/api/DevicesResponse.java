package com.ishsrec.gateway.api;

import java.util.List;
import java.util.Map;

public class DevicesResponse {

    private List<Map<String, Object>> devices;

    public DevicesResponse() {
    }

    public List<Map<String, Object>> getDevices() {
        return devices;
    }

    public void setDevices(List<Map<String, Object>> devices) {
        this.devices = devices;
    }
}

