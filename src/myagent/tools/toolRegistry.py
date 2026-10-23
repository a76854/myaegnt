from typing import Any
from myagent.tools import BashTool, Ctx7Tool, WebSearchTool
from myagent.core.config import ToolsSettings

TOOL_CLASSES: tuple[type[Any], ...] = (BashTool, Ctx7Tool, WebSearchTool)

def tools() -> list[dict[str, Any]]:
    """返回所有工具的实例列表。"""
    return [
        {
            "type": "function",
            "function":{
                
                "name": cls.name,
                "description": cls.description,
                "parameters": cls.schema
            },
        }
        for cls in TOOL_CLASSES
        ]

def build_tools(settings: ToolsSettings) -> dict[str, Any]:
    """根据配置构建工具实例列表。"""
    return {
        BashTool.name: BashTool(),
        Ctx7Tool.name: Ctx7Tool(api_key=settings.ctx7_api_key),
        WebSearchTool.name: WebSearchTool(api_key=settings.web_search_api_key)
    }
