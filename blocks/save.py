from datetime import datetime
import logging
import os
from aiogram import Bot
from constructor.blocks.block import Block
from ..data import Data
from .serial import SerialBlock


class SaveBlock(SerialBlock):
    def __init__(self, name: str, attr_str: str):
        super().__init__(name)
        self.attr_str = attr_str

    async def __call__(self, data: Data):
        await data.state.update_data({self.name: self.get_nested_attrs(data, self.attr_str)})
        await SerialBlock.__call__(self, data)


class SaveFileBlock(SerialBlock):
    def __init__(self, name: str):
        super().__init__(name)

    def register(self, next_block: Block, bot: Bot, user_files_path: str):
        super().register(next_block)
        self.bot: Bot = bot
        self.user_files_path: str = user_files_path

    async def __call__(self, data: Data):
        file = await self.bot.get_file(data.message.document.file_id)
        file_name = data.message.document.file_name

        user_id = data.message.from_user.id
        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        directory = f"{self.user_files_path}/{user_id}/{date_time}"
        path = directory + f"/{file_name}"
        os.makedirs(directory)

        await self.bot.download_file(file.file_path, path)
        await data.state.update_data({self.name: f"{date_time}/{file_name}"})

        await SerialBlock.__call__(self, data)