import json
from typing import List
from uuid import UUID
from aiokafka import AIOKafkaProducer

from Domain.Entities.outbox_message import OutboxMessage
from Application.message_producer_interface import MessageProducerInterface


class MessageProducer(MessageProducerInterface):
    _kafka_producer : AIOKafkaProducer
    _topic : str

    def __init__(self, kafka_producer : AIOKafkaProducer, topic : str = "order_created_messages"):
        self._kafka_producer = kafka_producer
        self._topic = topic

    async def send_message_batch(self, messages: List[OutboxMessage]) -> List[UUID]:
        message_ids = []
        try:
            for message in messages:
                try:
                    await self._kafka_producer.send_and_wait(
                        self._topic,
                        json.dumps(message.to_dict()).encode("utf-8"),
                        partition=0
                    )
                    message_ids.append(message.id)
                except Exception as e:
                    print(f"Failed to send message {message.id}: {e}")
        except Exception as e:
            print(f"Error with Kafka producer: {e}")
        finally:
            return message_ids
