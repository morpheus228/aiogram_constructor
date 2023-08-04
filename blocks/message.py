from aiogram import Bot

from ..errors import UnsatisfactoryEnviroment
from ..enviroment import Enviroment
from ..message_template import MessageTemplate
from ..data import Data
from .serial import SerialBlock


class MessageBlock(SerialBlock):
    def __init__(self, enviroment: Enviroment, template: MessageTemplate):
        super().__init__(enviroment)
        self.bot: Bot = enviroment.bot
        self.template: MessageTemplate = template

    async def __call__(self, data: Data):
        text, reply_markup =  self.template.render(data)
        await self.bot.send_message(chat_id=data.user.id, text=text, reply_markup=reply_markup)
        await SerialBlock.__call__(self, data=data)
        
    def check_enviroment(self):
        if self.enviroment.bot is None:
            raise UnsatisfactoryEnviroment(type(self), "bot")

