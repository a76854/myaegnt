from abc import ABC
from typing import Any, ClassVar

class BaseTool(ABC):
    name: ClassVar[str]
    description: ClassVar[str]
    schema: ClassVar[Any]

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the run method.")