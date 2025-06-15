import asyncio
from logging import getLogger

from Domain.Factories.payment_outbox_message_factory_interface import PaymentOutboxMessageFactoryInterface

from .unit_of_work_interface import UnitOfWorkInterface


logger = getLogger(__name__)

class PaymentPerformingService:

    _uow : UnitOfWorkInterface
    _payment_outbox_message_factory : PaymentOutboxMessageFactoryInterface

    def __init__ (self, uow : UnitOfWorkInterface,
                payment_outbox_message_factory : PaymentOutboxMessageFactoryInterface
    ):
        self._uow = uow
        self._payment_outbox_message_factory = payment_outbox_message_factory
    
    async def _process_payment(self) -> None:
        async with self._uow.start():
            logger.debug("UOW started")
            payment_inbox_message_repository = await self._uow.get_payment_inbox_message_repository()
            logger.debug("PaymentInboxMessageRepository got")
            payment_outbox_message_repository = await self._uow.get_payment_outbox_message_repository()
            logger.debug("PaymentOutboxMessageRepository got")
            bank_account_repository = await self._uow.get_bank_account_repository()
            logger.debug("BankAccountRepository got")
            inbox_messages = await payment_inbox_message_repository.get_unprocessed_messages()
            inbox_messages_ids = []
            for message in inbox_messages:
                inbox_messages_ids.append(message.id)
                try: 
                    bank_account = await bank_account_repository.get(message.user_id)
                    assert bank_account.balance >= message.amount
                    await bank_account_repository.replenish_balance(
                        user_id = bank_account.id,
                        amount = (-1) * message.amount
                    )
                    success_outbox_message = await self._payment_outbox_message_factory.create_success_message(order_id = message.id)
                    await payment_outbox_message_repository.add(success_outbox_message)
                except KeyError:
                    fail_outbox_message_by_account = await self._payment_outbox_message_factory.create_fail_message_by_account(order_id = message.id)
                    await payment_outbox_message_repository.add(fail_outbox_message_by_account)                 
                except AssertionError:
                    fail_outbox_message_by_balance = await self._payment_outbox_message_factory.create_fail_message_by_balance(order_id = message.id)
                    await payment_outbox_message_repository.add(fail_outbox_message_by_balance)
                except Exception as e:
                    logger.error("Exception while processing payments: %s}", str(e))
            await payment_inbox_message_repository.mark_as_processed(inbox_messages_ids)
                
    async def start_processing_payment(self) -> None:
        logger.debug("Func: start_processing_payment")
        while True:
            await self._process_payment()
            await asyncio.sleep(5)
