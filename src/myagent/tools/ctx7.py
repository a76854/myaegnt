from .basetool import BaseTool
from httpx import Client
from typing import Optional

class Ctx7Tool(BaseTool):
    name = "context7"
    description = "A tool for performing searches in the Context7 API."
    schema = {
        "type": "object",
        "properties": {
            "library_name": {
                "type": "string",
                "description": "The name of the library to search in."
            },
            "query": {
                "type": "string",
                "description": "The search query to be executed."
            }
        },
        "required": ["library_name", "query"]
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client: Client | None = None

    @property
    def client(self) -> Client:
        if hasattr(self, '_client'):
            self._client = Client(base_url="https://context7.com/api/v2", headers={"Authorization": f"Bearer {self.api_key}"})
        return self._client

    def run(self, library_name, query):
        try:
            response = self.client.get(f"/libs/search", 
                                       params={
                                           "libraryName": library_name, 
                                           "query": query})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}