import time
from .unit_of_work_interface import UnitOfWorkInterface
from .message_producer_interface import MessageProducerInterface


class MessageProcessor:
    _message_producer : MessageProducerInterface
    _uow : UnitOfWorkInterface

    def __init__ (self, message_producer : MessageProducerInterface, uow : UnitOfWorkInterface):
        self._message_producer = message_producer
        self._uow = uow

    async def start_producing(self) -> None:
        print("WWWWW")
        while True:
            async with self._uow.start():
                message_repo = await self._uow.get_outbox_message_repository()
                unprocessed_messages = await message_repo.get_unprocessed_messages()
                print(f"{len(unprocessed_messages)=}, {unprocessed_messages=}")
                published_ids = await self._message_producer.send_message_batch(unprocessed_messages)
                await message_repo.mark_as_processed(published_ids)
            time.sleep(5)

    # async def start_consuming(self) -> None:
    #     while True:
    #         async with self._uow.start():
    #             message_repo = await self._uow.get_outbox_message_repository()
    #             unprocessed_messages = await message_repo.get_unprocessed_messages()
    #             published_ids = await self._message_producer.send_message_batch(unprocessed_messages)
    #             await message_repo.mark_as_processed(published_ids)
    #         time.sleep(5)
    
