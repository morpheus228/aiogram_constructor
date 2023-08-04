from abc import abstractmethod

from aiogram.fsm.state import State
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..enviroment import Enviroment
from ..errors import UnsatisfactoryEnviroment
from .block import Block
from .serial import SerialBlock
from ..data import Data


class HandledBlock(SerialBlock):
    def __init__(self, enviroment: Enviroment):
        super().__init__(enviroment)
        self.router: Router = enviroment.router
        self.state: State = State(state=self.name, group_name=self.router.name)

    def check_enviroment(self):
        if self.enviroment.router is None:
            raise UnsatisfactoryEnviroment(type(self), "router")

    async def __call__(self, data: Data):
        await data.state.set_state(self.state)

    @abstractmethod
    def register(self, next_block: Block):
        super().register(self, next_block)

    async def handle(self, event: CallbackQuery|Message, state: FSMContext):
        await SerialBlock.__call__(self, Data(event=event, state=state))


class MessageHandledBlock(HandledBlock):
    def register(self, next_block: Block):
        super().register(self, next_block)
        self.router.message.register(self.handle, self.state)


class CallbackHandledBlock(HandledBlock):
    def register(self, next_block: Block):
        super().register(self, next_block)
        self.router.callback_query.register(self.handle, self.state)

