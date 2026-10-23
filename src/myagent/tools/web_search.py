from tavily import TavilyClient

from .basetool import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "A tool for performing web searches using the Tavily API."
    schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to be executed."
            }
        },
        "required": ["query"]
    }
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client : TavilyClient | None = None
    @property
    def client(self) -> TavilyClient:
        if self._client is None:
            self._client = TavilyClient(api_key=self.api_key)
        return self._client

    def run(self, query):
        try:
            response = self.client.search(query)
            return response
        except Exception as e:
            return {"error": str(e)}
