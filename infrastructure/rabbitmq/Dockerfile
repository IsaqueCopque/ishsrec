FROM rabbitmq:3-management

COPY rabbitmq.conf /etc/rabbitmq/
COPY enabled_plugins /etc/rabbitmq/
COPY definitions.json /etc/rabbitmq/

# 5672 -> AMQP
# 15672 -> Management UI
# 1883 -> MQTT
EXPOSE 5672 15672 1883