from abc import ABC, abstractmethod

from ..enviroment import Enviroment
from ..data import Data


class Block(ABC):
    def __init__(self, enviroment: Enviroment):
        self.enviroment: Enviroment = enviroment
        self.check_enviroment()

    @abstractmethod
    async def __call__(self, data: Data):
        pass

    @abstractmethod
    def check_enviroment(self):
        pass

    @staticmethod
    def get_nested_attrs(obj, attrs_str: str):
        for attr in attrs_str.split("."):
            obj = getattr(obj, attr)

        return obj