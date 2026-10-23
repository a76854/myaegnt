from abc import ABC, abstractmethod
from typing import Any, ClassVar


class BaseTool(ABC):
    name: ClassVar[str]
    description: ClassVar[str]
    schema: ClassVar[Any]

    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the run method.")
