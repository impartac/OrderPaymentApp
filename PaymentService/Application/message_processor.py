# import asyncio
# from logging import getLogger

# from Domain.Factories.payment_outbox_message_factory_interface import PaymentOutboxMessageFactoryInterface

# from .message_consumer_interface import MessageConsumerInterface
# from .unit_of_work_interface import UnitOfWorkInterface
# from .message_producer_interface import MessageProducerInterface

# logger = getLogger(__name__)

# class MessageProcessor:
#     _message_producer : MessageProducerInterface
#     _uow : UnitOfWorkInterface
#     _message_consumer: MessageConsumerInterface
#     _outbox_message_factory : PaymentOutboxMessageFactoryInterface

#     def __init__ (self, uow : UnitOfWorkInterface,
#                 message_consumer : MessageConsumerInterface,
#                 messape_producer : MessageProducerInterface,
#                 outbox_message_factory : PaymentOutboxMessageFactoryInterface
#     ):
#         self._message_consumer = message_consumer
#         self._uow = uow
#         self._message_producer = messape_producer
#         self._outbox_message_factory = outbox_message_factory

#     async def start_consuming(self) -> None:
#         logger.debug("Func: start_consuming")
#         while True:
#             async with self._uow.start():
#                 logger.debug("UOW started")
#                 payment_inbox_message_repository = await self._uow.get_payment_inbox_message_repository()
#                 logger.debug("InboxMessageRepository got")
#                 unprocessed_messages = await self._message_consumer.consume_batch()
#                 logger.debug("Unprocessed messages len = %s", len(unprocessed_messages))
#                 if unprocessed_messages:
#                     await asyncio.gather(*[
#                         payment_inbox_message_repository.add(message)
#                         for message in unprocessed_messages
#                     ])
#             await asyncio.sleep(5)
            
#     async def _process_payment(self) -> None:
#         async with self._uow.start():
#                 logger.info("UOW started")
#                 payment_inbox_message_repository = await self._uow.get_payment_inbox_message_repository()
#                 logger.info("PaymentInboxMessageRepository got")
#                 payment_outbox_message_repository = await self._uow.get_payment_outbox_message_repository()
#                 logger.info("PaymentOutboxMessageRepository got")
#                 bank_account_repository = await self._uow.get_bank_account_repository()
#                 logger.info("BankAccountRepository got")
#                 inbox_messages = await payment_inbox_message_repository.get_unprocessed_messages()
#                 inbox_messages_ids = []
#                 for message in inbox_messages:
#                     inbox_messages_ids.append(message.id)
#                     try: 
#                         bank_account = await bank_account_repository.get(message.user_id)
#                         assert bank_account.balance >= message.amount
#                         success_outbox_message = await self._outbox_message_factory.create_success_message(order_id = message.id)
#                         await payment_outbox_message_repository.add(success_outbox_message)
#                     except KeyError:
#                         fail_outbox_message_by_account = await self._outbox_message_factory.create_fail_message_by_account(order_id = message.id)
#                         await payment_outbox_message_repository.add(fail_outbox_message_by_account)
#                         await bank_account_repository.replenish_balance(
#                             user_id = bank_account.id,
#                             amount = (-1) * message.amount
#                         )
#                     except AssertionError:
#                         fail_outbox_message_by_balance = await self._outbox_message_factory.create_fail_message_by_balance(order_id = message.id)
#                         await payment_outbox_message_repository.add(fail_outbox_message_by_balance)
#                     except Exception as e:
#                         logger.error("Exception while processing payments: %s}", str(e))
#                 await payment_inbox_message_repository.mark_as_processed(inbox_messages_ids)

#     async def start_processing_payment(self) -> None:
#         logger.debug("Func: start_processing_payment")
#         while True:
#             await self._process_payment()
#             await asyncio.sleep(5)
            
#     async def _produce_messages(self) -> None:
#         async with self._uow.start():
#             payment_outbox_mesage_repository = await self._uow.get_payment_outbox_message_repository()
#             unprocessed_payment_outbox_messages = await payment_outbox_mesage_repository.get_unprocessed_messages()
#             print(f"{len(unprocessed_payment_outbox_messages)=}, {unprocessed_payment_outbox_messages=}")
#             published_ids = await self._message_producer.send_message_batch(unprocessed_payment_outbox_messages)
#             await payment_outbox_mesage_repository.mark_as_processed(published_ids)
            
#     async def start_producing(self) -> None:
#         logger.debug("Func: strart_producing")
#         while True:
#             await self._produce_messages()
#             await asyncio.sleep(5)
