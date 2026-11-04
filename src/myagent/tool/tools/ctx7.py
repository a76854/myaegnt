from typing import Any

from httpx import Client
from pydantic import BaseModel, Field

from .basetool import BaseTool


class Ctx7Args(BaseModel):
    library_name: str = Field(description="The name of the library to search in.")
    query: str = Field(description="The search query to be executed.")


class Ctx7Tool(BaseTool):
    name = "context7"
    description = "A tool for performing searches in the Context7 API."
    args_model = Ctx7Args

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client: Client | None = None

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(base_url="https://context7.com/api/v2", headers={"Authorization": f"Bearer {self.api_key}"})
        return self._client

    def run(self, library_name: str, query: str) -> Any:
        try:
            response = self.client.get("/libs/search",
                                       params={
                                           "libraryName": library_name,
                                           "query": query})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
