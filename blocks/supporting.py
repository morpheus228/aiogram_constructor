from .block import Block
from .serial import SerialBlock
from ..data import Data


class EndBlock(Block):
    def __init__(self):
        super().__init__(name='End')
    
    async def __call__(self, data: Data):
        await data.state.clear()


class StartBlock(SerialBlock):
    def __init__(self):
        super().__init__(name='Start')
