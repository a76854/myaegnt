from myagent.core.config import Settings
from myagent.core.llm import LLMClient


class Agent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm_client = LLMClient(self.settings)

    def agent_loop(self, messages):
        while True:

            response = self.llm_client.chat(messages, 
                                            stream=self.settings.STREAM, 
                                            reasoning_effort=self.settings.REASONING_EFFORT, 
                                            extra_body={"thinking": {"type": self.settings.THINKING_TYPE}})
            assistant_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_message})
