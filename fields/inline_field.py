from aiogram import Dispatcher, Router

from ..data import Data
from ..blocks import *
from ..message_template import MessageTemplate


class InlineField(Block):
    def __init__(self, name: str, template: MessageTemplate):
        self.request = MessageTemplateBlock(name + '_request', template)
        self.handling = CallbackHandledBlock(name + '_handling')
        self.rikmbt = RIKMBTBlock(name + '_rikmbt')
        self.saving = SaveBlock(name, 'callback.data')

    def register(self, next_block: Block, dp: Dispatcher, router: Router):
        self.request.register(self.handling, dp['sender'])
        self.handling.register(self.saving, router)
        self.saving.register(self.rikmbt)
        self.rikmbt.register(next_block)

    async def __call__(self, data: Data):
        await self.request(data)

        