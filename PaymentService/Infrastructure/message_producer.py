import json
from typing import List
from uuid import UUID
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from logging import getLogger

from Domain.Entities.payment_outbox_message import PaymentOutboxMessage
from Application.message_producer_interface import MessageProducerInterface


logger = getLogger(__name__)

class MessageProducer(MessageProducerInterface):
    _kafka_producer : AIOKafkaProducer
    _topic : str
    _is_running : bool

    def __init__(self, kafka_producer : AIOKafkaProducer, topic : str = "order_created_messages"):
        self._kafka_producer = kafka_producer
        self._topic = topic
        self._is_running = False 

    async def start(self):
        if not self._is_running:
            await self._kafka_producer.start()
            self._is_running = True
            logger.info("Kafka Producer started successfully")
        else:
            logger.warning("Kafka Producer is already running")

    async def stop(self):
        if self._is_running:
            await self._kafka_producer.stop()
            self._is_running = False
            logger.info("Kafka Producer stopped successfully")
        else:
            logger.warning("Kafka Producer is already stopped")

    async def send_message_batch(self, messages: List[PaymentOutboxMessage]) -> List[UUID]:
        message_ids = []
        for message in messages:
            try:
                await self._kafka_producer.send_and_wait(
                    self._topic,
                    json.dumps(message.to_dict()).encode("utf-8")
                )
                message_ids.append(message.id)
                logger.info(f"Message with ID {message.id} sent successfully.")
            except KafkaError as e: 
                logger.error(f"Failed to send message with ID {message.id}: {e}")
                raise  
        return message_ids