# AnAgentExample

一个从零手写的 **LLM Agent 最小实现**，用于教学。不依赖 LangChain / LlamaIndex，只用 `openai` SDK + `pydantic-settings`，把「模型 → 工具调用 → 结果回填 → 再推理」的闭环完整摊开。

项目名 `AnAgentExample`，Python 包名 `myagent`。

## 特性

- 多轮对话，完整携带消息历史
- OpenAI 兼容的 Function Calling（`tools` / `tool_choice` / `tool_call_id`）
- 三个内置工具：`bash`（本地命令）、`web_search`（Tavily）、`context7`（文档检索）
- 配置按前缀分组（`LLM_*` / `TOOLS_*`），互不干扰
- 工具元数据定义在类属性上，不实例化即可读取

## 快速开始

```bash
git clone https://github.com/<your-name>/AnAgentExample.git
cd AnAgentExample

uv sync
cp .env.example .env      # 填入 LLM_API_KEY 等
uv run src/myagent/main.py
```

输入 `exit` 退出。

## 配置

`pydantic-settings` 管理，按前缀分组：`settings.llm.*` / `settings.tools.*`。

| 变量 | 默认值 | 说明 |
|---|---|---|
| `LLM_MODEL` | `deepseek-flash` | 模型名 |
| `LLM_BASE_URL` | `https://api.deepseek.com` | OpenAI 兼容端点 |
| `LLM_API_KEY` | — | API Key |
| `LLM_STREAM` | `False` | 当前循环要求 `False` |
| `LLM_REASONING_EFFORT` | `high` | 推理强度 |
| `LLM_THINKING_TYPE` | `disabled` | 透传给 `extra_body.thinking` |
| `TOOLS_WEB_SEARCH_API_KEY` | — | Tavily Key |
| `TOOLS_CTX7_API_KEY` | — | Context7 Key |

优先级：**显式传参 > 环境变量 > `.env` > 默认值**。如果你在 shell 里 `export` 过同名变量，它会覆盖 `.env`——这是最常见的坑，排查先看 `echo $LLM_BASE_URL`。

## 执行流程

```
main.py (input → messages)
   └─ Agent.agent_loop(messages)
        ├─ LLMClient.chat(tools=..., tool_choice="auto")
        ├─ 无 tool_calls → 返回文本
        └─ 有 tool_calls
             ├─ messages += assistant(tool_calls)
             ├─ 执行工具
             ├─ messages += tool(tool_call_id, result)
             └─ 继续循环
```

Function Calling 三条铁律：assistant 的 `tool_calls` 要原样回填；每个 `tool_call_id` 必须有 `role: tool` 应答；`tool_choice` 不能传实例。

## 目录结构

```
src/myagent/
├── main.py              # 入口：维护 messages
├── agent/agent.py       # Agent 循环
├── core/config.py       # 前缀分组配置
├── core/llm.py          # OpenAI 兼容客户端
└── tools/
    ├── basetool.py      # BaseTool 契约
    ├── bash.py | web_search.py | ctx7.py
    └── toolRegistry.py  # schema 导出 + 实例构建

tests/unit_tests/        # config / tools / llm_client
```

## 新增工具

```python
class EchoTool(BaseTool):
    name = "echo"
    description = "原样返回输入文本"
    schema = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}

    def run(self, text: str) -> str:
        return text
```

然后在 `tools/__init__.py` 导出，在 `toolRegistry.py` 的 `TOOL_CLASSES` 和 `build_tools()` 里注册即可。

## 测试

```bash
uv run pytest tests -v              # 全部（llm_client_test 会真实请求模型）
uv run pytest tests -v -k "not llm_client"   # 只跑离线测试
```

## 已知限制

- `agent_loop` 是 `while True`，无轮数上限
- 不支持流式（`LLM_STREAM=True` 会抛错）
- 无上下文截断、无持久化
- `prompts.py` 尚未接入，messages 里没有 system 消息
- `BashTool` 用 `shell=True` + 子串黑名单，容易被绕过

## 安全提示

`BashTool` 会在宿主机真实执行模型生成的命令，仅限本地学习使用。`.env` 已在 `.gitignore` 中，切勿提交真实 Key。

## License

[MIT](LICENSE) © 2026 huiguo
