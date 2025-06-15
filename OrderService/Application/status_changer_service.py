import asyncio
from logging import getLogger

from Domain.Factories.payment_processed_inbox_message_factory_interface import PaymentProcessedInboxMessageFactoryInterface

from .unit_of_work_interface import UnitOfWorkInterface


logger = getLogger(__name__)

class StatusChangerService:

    _uow : UnitOfWorkInterface
    _payment_processed_inbox_message_factory : PaymentProcessedInboxMessageFactoryInterface

    def __init__ (self, uow : UnitOfWorkInterface,
                payment_processed_inbox_message_factory : PaymentProcessedInboxMessageFactoryInterface
    ):
        self._uow = uow
        self._payment_processed_inbox_message_factory = payment_processed_inbox_message_factory
    
    async def _process_payment(self) -> None:
        async with self._uow.start():
            logger.debug("UOW started")
            payment_processed_inbox_message_repository = await self._uow.get_payment_processed_inbox_message_repository()
            logger.debug("PaymentInboxMessageRepository got")
            order_repository = await self._uow.get_order_repository()
            logger.debug("OrderRepository got")
            inbox_messages = await payment_processed_inbox_message_repository.get_unprocessed_messages()
            inbox_messages_ids = []
            for message in inbox_messages:
                inbox_messages_ids.append(message.id)
                try: 
                    if message.is_success:
                        await order_repository.set_finished_status(order_id = message.id)
                    else:
                        await order_repository.set_cancelled_status(order_id = message.id)
                except Exception as e:
                    logger.error("Exception while processing payments: %s}", str(e))
            await payment_processed_inbox_message_repository.mark_as_processed(inbox_messages_ids)
                
    async def start_processing_payment(self) -> None:
        logger.debug("Func: start_processing_payment")
        while True:
            await self._process_payment()
            await asyncio.sleep(5)
