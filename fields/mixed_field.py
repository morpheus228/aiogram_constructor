from aiogram import Dispatcher, Router

from ..data import Data
from ..blocks import *
from ..message_template import MessageTemplate


class MixedField(Block):
    def __init__(self, 
                 name: str, 
                 inline_template: MessageTemplate,
                 reply_template: MessageTemplate):

        self.request_inline = MessageTemplateBlock(name + '_request_inline', inline_template)
        self.request_reply = MessageTemplateBlock(name + '_request_reply', reply_template)

        self.handling_inline = CallbackHandledBlock(name + '_handling_inline')
        self.handling_reply = MessageHandledBlock(name + '_handling_reply')

        self.rikmbt = RIKMBTBlock(name + '_rikmbt')
        self.rm = RMBlock(name + '_rm')

        self.saving_reply = SaveBlock(name, 'message.text')
        self.saving_inline = SaveBlock(name, 'callback.data')

        self.inline_router = RouterBlock(name + '_inline_router', 'callback.data')

    def register(self, next_block: Block, dp: Dispatcher, router: Router):
        self.request_inline.register(self.handling_inline, dp['sender'])
        self.handling_inline.register(self.inline_router, router)

        self.inline_router.register({
            lambda x: x == 'other': self.rm,
            None: self.saving_inline
        })
        
        self.saving_inline.register(self.rikmbt)
        self.rikmbt.register(next_block)

        self.rm.register(self.request_reply)
        self.request_reply.register(self.handling_reply, dp['sender'])
        self.handling_reply.register(self.saving_reply, router)
        self.saving_reply.register(next_block)

    async def __call__(self, data: Data):
        await self.request_inline(data)

        