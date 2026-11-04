from typing import Any

from pydantic import BaseModel, Field
from tavily import TavilyClient

from .basetool import BaseTool


class WebSearchArgs(BaseModel):
    query: str = Field(description="The search query to be executed.")


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "A tool for performing web searches using the Tavily API."
    args_model = WebSearchArgs

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client: TavilyClient | None = None

    @property
    def client(self) -> TavilyClient:
        if self._client is None:
            self._client = TavilyClient(api_key=self.api_key)
        return self._client

    def run(self, query: str) -> Any:
        try:
            return self.client.search(query)
        except Exception as e:
            return {"error": str(e)}
