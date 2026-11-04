from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel

from myagent.core.config import WORK_DIR


class BaseTool(ABC):
    """所有工具的基类。

    子类只需要声明三样东西：
      - name / description：给模型看的元数据，类属性，不实例化也能读；
      - args_model：参数模型，schema 由它自动生成，同时用于运行时校验。

    注意：schema 不要手写，`__init_subclass__` 会在子类定义完成后自动填好，
    这样参数只有一个事实来源（args_model），改参数不用改两份。
    """

    name: ClassVar[str]
    description: ClassVar[str]
    args_model: ClassVar[type[BaseModel]]
    schema: ClassVar[dict[str, Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.schema = cls.args_model.model_json_schema()

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the run method.")


def safe_path(path: str) -> Path:
    """确保路径在工作目录下，防止访问系统敏感目录。"""
    abs_path = (WORK_DIR / path).resolve()
    if not str(abs_path).startswith(str(WORK_DIR)):
        raise ValueError(f"Access to path '{path}' is denied.")
    return abs_path
