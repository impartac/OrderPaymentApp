import asyncio
from logging import getLogger

from .unit_of_work_interface import UnitOfWorkInterface
from .message_producer_interface import MessageProducerInterface

logger = getLogger(__name__)

class MessageProducerService:
    _message_producer : MessageProducerInterface
    _uow : UnitOfWorkInterface

    def __init__ (self, uow : UnitOfWorkInterface,
                message_producer : MessageProducerInterface,
    ):
        self._message_producer = message_producer
        self._uow = uow
    
    
    async def _produce_messages(self) -> None:
        # try:
        async with self._uow.start():
            logger.info("UOW started for producing messages")
            payment_outbox_mesage_repository = await self._uow.get_payment_outbox_message_repository()
            logger.info("Payment outbox message repository retrieved")
            unprocessed_payment_outbox_messages = await payment_outbox_mesage_repository.get_unprocessed_messages()
            logger.info(f"Found {len(unprocessed_payment_outbox_messages)} unprocessed outbox messages")
            if not unprocessed_payment_outbox_messages:
                logger.info("No unprocessed outbox messages to send")
                return  
            logger.info(f"Producing {len(unprocessed_payment_outbox_messages)} messages") 
            published_ids = await self._message_producer.send_message_batch(unprocessed_payment_outbox_messages)
            logger.info(f"Message batch sent successfully")
            
            await payment_outbox_mesage_repository.mark_as_processed(published_ids)
            logger.info(f"Marked messages as processed: {published_ids}")
            
            logger.info("UOW committed after producing messages")
                
        # except Exception as e:
        #     logger.error(f"Error while producing messages:{str(e)}") 
        #     logger.debug("UOW rollback triggered")
        #     raise 
    
    async def start_producing(self) -> None:
        logger.info("Func: start_producing")
        try:
            await self._message_producer.start()
            logger.info("Message producer STARTED")
            while True:
                try:
                    await self._produce_messages()
                except Exception as e:
                    logger.error(f"Error during message production: {e}")
                await asyncio.sleep(5) 
        except Exception as e:
            logger.error("Error during message producer setup/teardown:")
        finally:
            await self._message_producer.stop()
            logger.info("Message producer STOPPED")
    