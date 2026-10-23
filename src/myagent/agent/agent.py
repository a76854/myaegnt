from myagent.core.config import Settings, LLMSettings, ToolsSettings
from myagent.core.llm import LLMClient
from myagent.tools import BaseTool
from myagent.tools.toolRegistry import tools, build_tools

import json
from typing import Any

MAX_TOOL_USE_ATTEMPTS = 5

class Agent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm_settings: LLMSettings = settings.llm
        self.tools_settings: ToolsSettings = settings.tools
        self.llm_client = LLMClient(self.llm_settings)
        self._tool_impls: dict[str, BaseTool] | None = None

    def _tool_instances(self) -> dict[str, BaseTool]:
        if self._tool_impls is None:
            self._tool_impls = build_tools(self.tools_settings)
        return self._tool_impls

    def agent_loop(self, messages):
        while True:
            for _ in range(MAX_TOOL_USE_ATTEMPTS):
                response = self.llm_client.chat(messages, 
                                                stream=self.llm_settings.stream, 
                                                reasoning_effort=self.llm_settings.reasoning_effort, 
                                                extra_body={"thinking": {"type": self.llm_settings.thinking_type}},
                                                tools=tools(),
                                                tool_choice=self._tool_instances())
                msg = response.choices[0].message

                if not msg.tool_calls:
                    messages.append({"role": "assistant", "content": msg.content})
                    return msg.content
                messages.append({
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [
                        {
                            "id": c.id,
                            "type": "function",
                            "function": {"name": c.function.name, "arguments": c.function.arguments},
                        }
                        for c in msg.tool_calls
                    ],
                })
                response = self.llm_client.chat(messages, 
                                                stream=self.llm_settings.stream, 
                                                reasoning_effort=self.llm_settings.reasoning_effort, 
                                                extra_body={"thinking": {"type": self.llm_settings.thinking_type}})
                msg = response.choices[0].message

                if not msg.tool_calls:
                    messages.append({"role": "assistant", "content": msg.content})
                    return messages
                messages.append({
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [
                        {
                            "id": c.id,
                            "type": "function",
                            "function": {"name": c.function.name, "arguments": c.function.arguments},
                        }
                        for c in msg.tool_calls
                    ],
                })

                impls = self._tool_instances()
                for call in msg.tool_calls:
                    tool_name = call.function.name
                    if tool_name in impls:
                        tool_impl = impls[tool_name]
                        tool_result = self._execute(impls, tool_name, call.function.arguments)
                        messages.append({
                            "role": "tool",
                            "name": tool_name,
                            "content": json.dumps(tool_result)
                        })
                    else:
                        messages.append({
                            "role": "tool",
                            "name": tool_name,
                            "content": f"Error: Tool '{tool_name}' not found."
                        })

    @staticmethod
    def _execute(impls: dict[str, BaseTool], name: str, raw_args: str) -> Any:
        try:
            args = json.loads(raw_args or "{}")
        except json.JSONDecodeError as e:
            return {"error": f"invalid JSON arguments: {e}"}
        tool = impls.get(name)
        if tool is None:
            return {"error": f"unknown tool: {name}"}
        try:
            return tool.run(**args)
        except Exception as e:                    # 工具异常要变成文本回给模型，别让循环崩
            return {"error": f"{type(e).__name__}: {e}"}


            
