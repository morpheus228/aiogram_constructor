from abc import abstractmethod

from .block import Block
from ..data import Data


class SerialBlock(Block):
    def register(self, next_block: Block):
        self.next_block = next_block

    async def __call__(self, data: Data):
        await self.next_block(data=data)
