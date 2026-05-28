package com.ishsrec.gateway.controller;

import java.util.Map;

import com.ishsrec.gateway.api.DevicesResponse;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.web.client.RestTemplate;

import com.ishsrec.gateway.api.ResidentLoginResponse;
import com.ishsrec.gateway.controller.GatewayAuthController;

@WebMvcTest(GatewayAuthController.class)
public class GatewayAuthControllerTest {
        @Autowired
        private MockMvc mockMvc;

        @MockBean
        private RestTemplate restTemplate;

        /*
        * A complete login response must include the resident's id, name, email, and token
         */
        @Test
        void shouldLoginSuccessfully() throws Exception {

                ResidentLoginResponse response = new ResidentLoginResponse();
                response.setToken("abc123");

                Map<String, Object> resident = Map.of("id", 1, "name", "John", "email",
                 "blala@email.com", "password", "ahs72k","token","tokenvalue");
                response.setResident(resident);

                ResponseEntity<ResidentLoginResponse> entity = ResponseEntity.ok(response);

                Mockito.when(
                                restTemplate.postForEntity(
                                                Mockito.anyString(),
                                                Mockito.any(),
                                                Mockito.eq(ResidentLoginResponse.class)))
                                .thenReturn(entity);

                Mockito.when(
                                restTemplate.getForEntity(
                                                Mockito.anyString(),
                                                Mockito.eq(DevicesResponse.class)))
                                .thenReturn(ResponseEntity.ok(new DevicesResponse()));

                String json = """
                                {
                                  "email":"test@test.com",
                                  "password":"123"
                                }
                                """;
                                        
                mockMvc.perform(MockMvcRequestBuilders.post("/api/login")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(json))
                                .andExpect(MockMvcResultMatchers.status().isOk())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.token").isNotEmpty())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.resident.name").isNotEmpty())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.resident.email").isNotEmpty())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.resident.id").isNotEmpty())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.devices").isArray());
        }

}
