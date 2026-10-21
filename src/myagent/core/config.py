from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LLM_MODEL: str = "deepseek-flash"
    LLM_BASE_URL: str = "https://api.deepseek.com"
    LLM_API_KEY: str = "YOUR_API_KEY_HERE"

    model_config = SettingsConfigDict(env_file = ".env")