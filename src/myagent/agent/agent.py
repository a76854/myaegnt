import json
from typing import Any

from pydantic import ValidationError

from myagent.core.config import LLMSettings, Settings, ToolsSettings
from myagent.core.llm import LLMClient
from myagent.tool.tool_registry import build_tools, tools
from myagent.tool.tools import BaseTool

MAX_TOOL_RESULT_CHARS = 8000


class Agent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm_settings: LLMSettings = settings.llm
        self.tools_settings: ToolsSettings = settings.tools
        self.llm_client = LLMClient(self.llm_settings)
        self._tool_impls: dict[str, BaseTool] | None = None

    def _tool_instances(self) -> dict[str, BaseTool]:
        """首次真正执行工具时才实例化（此时才需要 API key）。"""
        if self._tool_impls is None:
            self._tool_impls = build_tools(self.tools_settings)
        return self._tool_impls

    def agent_loop(self, messages: list[dict]) -> str:
        if self.llm_settings.stream:
            # 带工具调用的循环需要完整响应（choices/message/tool_calls），流式拿不到
            raise ValueError("agent_loop 暂不支持流式，请设置 LLM_STREAM=False")

        tool_specs = tools()  # 工具的 schema 列表：类属性，不需要实例化/API key

        while True:
            response = self.llm_client.chat(
                messages,
                stream=False,
                reasoning_effort=self.llm_settings.reasoning_effort,
                extra_body={"thinking": {"type": self.llm_settings.thinking_type}},
                tools=tool_specs,
                tool_choice="auto",
            )
            msg = response.choices[0].message

            # 模型不再调用工具 → 这就是最终回答
            if not msg.tool_calls:
                messages.append({"role": "assistant", "content": msg.content})
                return msg.content

            # ① 先把带 tool_calls 的 assistant 消息原样回填（必须带 id/name/arguments）
            messages.append({
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [
                    {
                        "id": c.id,
                        "type": "function",
                        "function": {
                            "name": c.function.name,
                            "arguments": c.function.arguments,
                        },
                    }
                    for c in msg.tool_calls
                ],
            })

            # ② 逐个执行，并按 tool_call_id 回填结果
            impls = self._tool_instances()
            for call in msg.tool_calls:
                print(f"Executing tool: {call.function.name} with arguments: {call.function.arguments}")
                result = self._execute(impls, call.function.name, call.function.arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, ensure_ascii=False, default=str)[:MAX_TOOL_RESULT_CHARS],
                })

            # ③ 继续 while 循环，把工具结果交给模型，直到它不再调用工具

    @staticmethod
    def _execute(impls: dict[str, BaseTool], name: str, raw_args: str) -> Any:
        tool = impls.get(name)
        if tool is None:
            return {"error": f"unknown tool: {name}"}

        # 模型给的参数是不可信输入：先用工具的 args_model 校验/补齐类型，
        # 校验失败就把可读的错误回给模型，而不是抛 TypeError。
        try:
            args = tool.args_model.model_validate_json(raw_args or "{}")
        except ValidationError as e:
            return {"error": f"invalid arguments for {name}: {e}"}

        try:
            return tool.run(**args.model_dump())
        except Exception as e:  # 工具异常转成文本回给模型，别让循环崩掉
            return {"error": f"{type(e).__name__}: {e}"}
