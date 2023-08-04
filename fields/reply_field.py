from aiogram import Dispatcher, Router

from ..data import Data
from ..blocks import *
from ..message_template import MessageTemplate


class ReplyField(Block):
    def __init__(self, name: str, template: MessageTemplate):
        self.request = MessageTemplateBlock(name + '_request', template)
        self.handling = MessageHandledBlock(name + '_handling')
        self.saving = SaveBlock(name, 'message.text')

    def register(self, next_block: Block, dp: Dispatcher, router: Router):
        self.request.register(self.handling, dp['sender'])
        self.handling.register(self.saving, router)
        self.saving.register(next_block)

    async def __call__(self, data: Data):
        await self.request(data)

        