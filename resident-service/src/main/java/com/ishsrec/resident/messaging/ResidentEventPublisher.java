package com.ishsrec.resident.messaging;

import com.ishsrec.resident.model.Resident;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Component
public class ResidentEventPublisher {

    private final RabbitTemplate rabbitTemplate;

    public ResidentEventPublisher(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void publishResidentCreated(Resident resident) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("id", resident.getId());
        payload.put("name", resident.getName());
        // payload.put("status", resident.getStatus());

        Map<String, Object> event = new HashMap<>();
        event.put("eventType", "resident.created");
        event.put("eventId", UUID.randomUUID().toString());
        event.put("timestamp", Instant.now().toString());
        event.put("payload", payload);

        rabbitTemplate.convertAndSend(
                RabbitConfig.RESIDENT_EVENTS_EXCHANGE,
                "resident.created",
                event
        );
    }
}

