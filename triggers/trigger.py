from abc import abstractmethod

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..blocks.block import Block
from ..data import Data


class Trigger:
    def __init__(self, name: str):
        self.name: str = name
        self.next_block: Block = None

    @abstractmethod
    def register(self, next_block: Block):
        self.next_block: Block = next_block

    @abstractmethod
    async def handle(self, *args, **kwargs):
        pass
    
    
class MessageTrigger(Trigger):
    def register(self, next_block: Block, router: Router, filters: list):
        Trigger.register(self, next_block)
        router.message.register(self.handle, *filters)

    async def handle(self, message: Message, state: FSMContext):
        data = Data(event=message, state=state)
        await self.next_block(data)


class CallbackTrigger(Trigger):
    def register(self, next_block: Block, router: Router, filters: list):
        Trigger.register(self, next_block)
        router.callback_query.register(self.handle, *filters)
    
    async def handle(self, callback: CallbackQuery, state: FSMContext):
        data = Data(event=callback, state=state)
        await self.next_block(data)
