import asyncio
import uvicorn
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


from Infrastructure.Config.config import settings,session_maker
from Infrastructure.Factories.payment_processed_inbox_mesage_factory import PaymentProcessedInboxMessage, PaymentProcessedInboxMessageFactory
from Infrastructure.Mappers.payment_processed_inbox_message_mapper import PaymentProcessedInboxMessage, PaymentProcessedInboxMessageMapper
from Infrastructure.message_consumer import MessageConsumer
from Infrastructure.unit_of_work import UnitOfWork
from Infrastructure.Factories.order_created_outbox_message_factory import OrderCreatedOutboxMessageFactory
from Infrastructure.message_producer import MessageProducer

from Application.message_consumer_service import MessageConsumerService
from Application.message_producer_service import MessageProducerService
from Application.status_changer_service import StatusChangerService
from Application.unit_of_work_interface import UnitOfWorkInterface

# ------------------------------------------------------------------------------------------
async def _get_unit_of_work() -> UnitOfWorkInterface:
    return UnitOfWork(
        session_factory = session_maker
    )

async def _get_kafka_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.KAFKA_PAYMENT_MESSAGE_TOPIC,
        bootstrap_servers = settings.KAFKA_URL,
        group_id='xuesos2'
    )
    
async def _get_payment_processed_inbox_message_factory() -> PaymentProcessedInboxMessageFactory:
    return PaymentProcessedInboxMessageFactory()

async def _get_order_created_outbox_message_factory() -> OrderCreatedOutboxMessageFactory:
    return OrderCreatedOutboxMessageFactory()

async def _get_payment_processed_inbox_message_mapper() -> PaymentProcessedInboxMessageMapper:
    payment_inbox_message_factory = await _get_payment_processed_inbox_message_factory()
    return PaymentProcessedInboxMessageMapper(
        factory = payment_inbox_message_factory
    )
async def _get_message_consumer() -> MessageConsumer:
    kafka_consumer = await _get_kafka_consumer()
    payment_processed_inbox_message_mapper = await _get_payment_processed_inbox_message_mapper()
    return MessageConsumer(
        kafka_consumer = kafka_consumer,
        payment_processed_inbox_message_mapper = payment_processed_inbox_message_mapper,
        topic = settings.KAFKA_PAYMENT_MESSAGE_TOPIC
    )
async def _get_message_consumer_service() -> MessageConsumerService:
    uow = await _get_unit_of_work()
    message_consumer = await _get_message_consumer()
    return MessageConsumerService(
        uow = uow,
        message_consumer = message_consumer
    )
# ------------------------------------------------------------------------------------------

async def _get_kafka_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers = settings.KAFKA_URL,
    )

async def _get_message_producer() -> MessageProducer:
    kafka_producer = await _get_kafka_producer()
    return MessageProducer(
        kafka_producer = kafka_producer,
        topic = settings.KAFKA_ORDER_MESSAGES_TOPIC
    )
    
async def _get_message_producer_service() -> MessageProducerService:
    uow = await _get_unit_of_work()
    message_producer = await _get_message_producer()
    return MessageProducerService(
        uow = uow,
        message_producer = message_producer
    )
# ------------------------------------------------------------------------------------------
async def _get_status_changer_service() -> StatusChangerService:
    uow = await _get_unit_of_work()
    payment_processed_inbox_message_factory = await _get_payment_processed_inbox_message_factory()
    return StatusChangerService(
        uow = uow,
        payment_processed_inbox_message_factory = payment_processed_inbox_message_factory
    )



async def main():
    message_producer_service = await _get_message_producer_service()
    message_consumer_service = await _get_message_consumer_service()
    status_changer_service = await _get_status_changer_service()
    
    asyncio.create_task(message_consumer_service.start_consuming())
    asyncio.create_task(status_changer_service.start_processing_payment())
    asyncio.create_task(message_producer_service.start_producing())

    config = uvicorn.Config("Presentation.app:app", host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()
    
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
