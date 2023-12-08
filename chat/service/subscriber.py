"""
subscriber.py

This script subscribes to a RabbitMQ exchange and processes incoming messages.
"""

import asyncio
import json

from aio_pika import connect, ExchangeType
from aio_pika.abc import AbstractIncomingMessage
from channels.layers import get_channel_layer
from django.conf import settings


async def on_message(message: AbstractIncomingMessage) -> None:
    """
    Callback function to handle incoming messages from RabbitMQ.

    Args:
        message (AbstractIncomingMessage): The incoming message.

    Returns:
        None
    """
    async with message.process():
        print(f" [x] Received message {message!r}")

        # Deserialize the message body
        message_obj = json.loads(message.body)

        # Extract the purpose of the message
        purpose = message_obj["purpose"]

        if purpose == "new_chat_message":
            # Extract relevant data from the message
            chat_id = message_obj["chat_id"]
            message_content = message_obj["message"]
            sender = message_obj["sender"]

            # Generate the WebSocket room_name for the chat
            room_name = f"chat_{chat_id}"

            # Construct data to be sent to the WebSocket consumers
            data = {
                "type": "chat.message",
                "data": {
                    "purpose": "new_chat_message",
                    "message": message_content,
                    "sender": sender,
                },
            }

            print("DATA:", data)

            # Get the channel layer and send the data to the WebSocket room
            channel_layer = get_channel_layer()
            await channel_layer.group_send(room_name, data)

            print(f" [x] Sent new message notification to WebSocket")


async def main() -> None:
    """
    Main function to set up the RabbitMQ consumer.

    Returns:
        None
    """
    # Perform connection to RabbitMQ server
    connection = await connect(f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@127.0.0.1/")
    
    async with connection:
        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # Declare a fanout exchange
        exchange_name = "whatsapp_chat"
        exchange_type = ExchangeType.FANOUT
        exchange = await channel.declare_exchange(exchange_name, exchange_type)

        # Declare a durable queue
        queue_name = "whatsapp_chat"
        queue = await channel.declare_queue(queue_name)

        # Bind the queue to the exchange
        await queue.bind(exchange, routing_key="")

        # Start consuming messages from the queue
        await queue.consume(on_message)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
