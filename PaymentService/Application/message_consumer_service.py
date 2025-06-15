import asyncio
from logging import getLogger

from .message_consumer_interface import MessageConsumerInterface
from .unit_of_work_interface import UnitOfWorkInterface


logger = getLogger(__name__)

class MessageConsumerService:
    _uow : UnitOfWorkInterface
    _message_consumer: MessageConsumerInterface

    def __init__ (self, uow : UnitOfWorkInterface,
                message_consumer : MessageConsumerInterface,
    ):
        self._uow = uow
        self._message_consumer = message_consumer
        
    async def _consume(self) -> None:
        async with self._uow.start():
            logger.debug("UOW started")
            payment_inbox_message_repository = await self._uow.get_payment_inbox_message_repository()
            logger.debug("InboxMessageRepository got")
            unprocessed_messages = await self._message_consumer.consume_batch()
            logger.debug("Unprocessed messages len = %s", len(unprocessed_messages))
            if unprocessed_messages:
                await asyncio.gather(*[
                    payment_inbox_message_repository.add(message)
                    for message in unprocessed_messages
                ])
    
    async def start_consuming(self) -> None:
        logger.debug("Func: start_consuming")
        try:
            await self._message_consumer.start() 
            logger.info("Consumer STARTED")
            while True:
                try:
                    await self._consume()
                except Exception as e:
                    logger.error(f"Error during consumption: {e}") 
                await asyncio.sleep(5) 
        except Exception as e:
            logger.exception("Error during consumer setup/teardown:")
        finally:
            await self._message_consumer.stop() 
            logger.info("Consumer STOPPED")