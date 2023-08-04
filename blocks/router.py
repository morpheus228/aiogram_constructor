from abc import abstractmethod
from typing import Callable, Dict

from .block import Block
from ..data import Data


class RouterBlock(Block):
    def __init__(self, name: str, condition_object_str: str):
        Block.__init__(self, name)
        self.condition_object_str = condition_object_str

    def register(self, routes: Dict[Callable, Block]):
        self.routes: Dict[function, Block] = routes
    
    async def __call__(self, data: Data):
        condition_object = self.get_nested_attrs(data, self.condition_object_str)

        for condition in self.routes.keys():

            if (condition is not None) and (condition(condition_object)):
                await self.routes[condition](data)
                break

        else:
            await self.routes[None](data)