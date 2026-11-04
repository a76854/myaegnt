from collections.abc import Callable
from typing import Any

from myagent.core.config import ToolsSettings
from myagent.tool.tools import (
    BaseTool,
    BashTool,
    Ctx7Tool,
    EditFile,
    Glob,
    ReadFile,
    WebSearchTool,
    WriteFile,
)

# 工具注册表：唯一的事实来源。新增工具只需在这里加一行工厂，
# TOOL_CLASSES 和 build_tools 都会自动跟上，不会再漏改第二处。
_TOOL_FACTORIES: dict[type[BaseTool], Callable[[ToolsSettings], BaseTool]] = {
    BashTool: lambda _settings: BashTool(),
    Ctx7Tool: lambda settings: Ctx7Tool(api_key=settings.ctx7_api_key),
    WebSearchTool: lambda settings: WebSearchTool(api_key=settings.web_search_api_key),
    ReadFile: lambda _settings: ReadFile(),
    WriteFile: lambda _settings: WriteFile(),
    EditFile: lambda _settings: EditFile(),
    Glob: lambda _settings: Glob(),
}

TOOL_CLASSES: tuple[type[BaseTool], ...] = tuple(_TOOL_FACTORIES)


def tools() -> list[dict[str, Any]]:
    """返回 Function Calling 的工具定义（只读类属性，不实例化）。"""
    return [
        {
            "type": "function",
            "function": {
                "name": cls.name,
                "description": cls.description,
                "parameters": cls.schema,  # 由 args_model 自动生成
            },
        }
        for cls in TOOL_CLASSES
    ]


def build_tools(settings: ToolsSettings) -> dict[str, BaseTool]:
    """按配置构造工具实例；需要 API key 的工具在这里注入凭证。"""
    return {cls.name: factory(settings) for cls, factory in _TOOL_FACTORIES.items()}
