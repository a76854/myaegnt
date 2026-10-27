from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar

from myagent.core.config import WROK_DIR


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

def safe_path(path: str) -> Path:
    """确保路径在工作目录下，防止访问系统敏感目录。"""
    abs_path = (WROK_DIR / path).resolve()
    if not str(abs_path).startswith(str(WROK_DIR)):
        raise ValueError(f"Access to path '{path}' is denied.")
    return abs_path
