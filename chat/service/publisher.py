"""
publisher.py

This script publishes messages to a RabbitMQ exchange.
"""

import asyncio
import json
from django.conf import settings
from aio_pika import DeliveryMode, ExchangeType, Message, connect

async def publish(data: dict) -> None:
    """
    Publish a message to a RabbitMQ exchange.

    Args:
        data (dict): The data to be published.

    Returns:
        None
    """
    # Perform connection to RabbitMQ server
    connection = await connect(f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@127.0.0.1/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declare the exchange (Fanout type)
        exchange = await channel.declare_exchange(
            "whatsapp_chat",
            ExchangeType.FANOUT,
        )

        # Encoding the message before publishing
        message_body = json.dumps(data).encode()

        # Create a Message instance
        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        # Sending the message to the exchange with an empty routing key
        await exchange.publish(message, routing_key="")

        print(f" [x] Sent {message}")

if __name__ == "__main__":
    # Run the publish function using asyncio
    asyncio.run(publish())
