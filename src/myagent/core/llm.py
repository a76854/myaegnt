from openai import OpenAI
from myagent.core.config import LLMSettings

class LLMClient:
    def __init__(self, settings: LLMSettings):
        self.settings = settings
        self.client = OpenAI(
            api_key=self.settings.api_key,
            base_url=self.settings.base_url
        )

    def chat(self, messages: list, stream=False, reasoning_effort="high", extra_body=None, tools=None, tool_choice=None):
        kargs = {}
        if tools is not None:
            kargs["tools"] = tools
        if tool_choice is not None:
            kargs["tool_choice"] = tool_choice
        if extra_body is not None:
            kargs["extra_body"] = extra_body
        response = self.client.chat.completions.create(
            model = self.settings.model,
            messages = messages,
            stream = stream,
            reasoning_effort = reasoning_effort,
            **kargs
        )
        return response
