package com.ishsrec.resident.messaging;

import org.springframework.amqp.core.TopicExchange;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitConfig {

    public static final String RESIDENT_EVENTS_EXCHANGE = "resident.events";

    @Bean
    public TopicExchange residentEventsExchange() {
        return new TopicExchange(RESIDENT_EVENTS_EXCHANGE, true, false);
    }
}

