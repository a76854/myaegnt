import os
from openai import OpenAI
from myagent.core.config import Settings
from typing import Optional, Dict, Any

class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def chat(self, messages: list, stream=False, reasoning_effort="high", extra_body=None):
        client = OpenAI(
            api_key=self.settings.LLM_API_KEY,
            base_url=self.settings.LLM_BASE_URL
        )
        response = client.chat.completions.create(
            model = self.settings.LLM_MODEL,
            messages = messages,
            stream = stream,
            reasoning_effort = reasoning_effort,
            extra_body = extra_body or {"thinking": {"type": "enabled"}}
        )
        return response
