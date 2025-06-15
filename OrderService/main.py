import asyncio
import uvicorn
from aiokafka import AIOKafkaProducer

from Infrastructure.Config.config import settings,session_maker
from Infrastructure.unit_of_work import UnitOfWork
from Infrastructure.message_producer import MessageProducer

from Application.message_processor import MessageProcessor


async def main():
    uow = UnitOfWork(session_factory = session_maker)
    
    kafka_producer = AIOKafkaProducer(bootstrap_servers = settings.KAFKA_URL)
    
    await kafka_producer.start()

    message_producer = MessageProducer(
        kafka_producer = kafka_producer,
        topic = settings.KAFKA_ORDER_MESSAGES_TOPIC
    )

    processor = MessageProcessor(
        message_producer = message_producer,
        uow = uow
    )

    asyncio.create_task(processor.start_producing())

    config = uvicorn.Config("Presentation.app:app", host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()
    
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        print("Stopping the application...")
    finally:
        await kafka_producer.stop()

if __name__ == "__main__":
    asyncio.run(main())
