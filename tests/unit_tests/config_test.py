import pytest
from myagent.core.config import Settings

def test_settings_defaults():
    settings = Settings()
    assert settings.LLM_MODEL == "deepseek-flash"
    assert settings.LLM_BASE_URL == "https://api.deepseek.com"
    assert settings.LLM_API_KEY != "YOUR_API_KEY_HERE"