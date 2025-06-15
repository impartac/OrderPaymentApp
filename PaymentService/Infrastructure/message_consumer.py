import json

from typing import List
from aiokafka import AIOKafkaConsumer
from logging import getLogger

from Domain.Entities.payment_inbox_message import PaymentInboxMessage

from Application.message_consumer_interface import  MessageConsumerInterface

from .Mappers.payment_inbox_message_mapper import PaymentInboxMessageMapper


logger = getLogger(__name__)

class MessageConsumer(MessageConsumerInterface):
    kafka_consumer : AIOKafkaConsumer
    _topic : str
    _payment_inbox_message_mapper: PaymentInboxMessageMapper

    def __init__(self, kafka_consumer : AIOKafkaConsumer,
                payment_inbox_message_mapper : PaymentInboxMessageMapper,
                topic : str = "order_created_messages"):
        self.kafka_consumer = kafka_consumer
        self._topic = topic
        self._payment_inbox_message_mapper = payment_inbox_message_mapper

    async def consume_batch(self, batch_size: int = 64) -> List[PaymentInboxMessage]:
        logger.debug(f"Message consuming batch fucntion")
        raw_messages = await self.kafka_consumer.getmany(
            max_records=batch_size,
            timeout_ms=1000
        )
        logger.debug(f"Got raw messages = {raw_messages}")
        messages_batch = []
        for partition_messages in raw_messages.values():
            messages_batch.append(partition_messages)
        logger.debug(f"Got messages_batch {messages_batch}")
        domain_messages: List[PaymentInboxMessage] = []
        for msg in messages_batch:
            logger.info(f"Got message {msg}")
            domain_message = await self._payment_inbox_message_mapper.map_from_dict(json.loads(msg[0].value.decode('utf-8')))
            domain_messages.append(domain_message)
        logger.debug(f"Got domain messages {domain_messages}")
        return domain_messages

    async def start(self):
        await self.kafka_consumer.start()
        
    async def stop(self):
        await self.kafka_consumer.stop()