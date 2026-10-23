import pytest

from myagent.core.config import LLMSettings, Settings, WebSearchSettings


LLM_ENV_KEYS = (
    "LLM_MODEL",
    "LLM_BASE_URL",
    "LLM_API_KEY",
    "LLM_STREAM",
    "LLM_REASONING_EFFORT",
    "LLM_THINKING_TYPE",
)


def test_llm_settings_defaults(monkeypatch):
    for key in LLM_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    settings = LLMSettings(_env_file=None)  # 不读 .env，只看类默认值

    assert settings.model == "deepseek-flash"
    assert settings.base_url == "https://api.deepseek.com"
    assert settings.api_key == "YOUR_API_KEY_HERE"
    assert settings.stream is False
    assert settings.reasoning_effort == "high"
    assert settings.thinking_type == "disabled"


def test_env_prefix_is_isolated(monkeypatch):
    monkeypatch.setenv("WEB_SEARCH_ENGINE", "Bing")
    monkeypatch.setenv("LLM_MODEL", "some-model")

    assert WebSearchSettings().engine == "Bing"
    assert LLMSettings().model == "some-model"
    # 两个分组各读各的前缀，互不干扰
    assert WebSearchSettings().engine != LLMSettings().model


def test_settings_aggregates_groups(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "deepseek-flash")
    monkeypatch.setenv("WEB_SEARCH_ENGINE", "Tavily")

    settings = Settings()

    assert settings.llm.model == "deepseek-flash"
    assert settings.web_search.engine == "Tavily"


def test_bool_parsing(monkeypatch):
    monkeypatch.setenv("LLM_STREAM", "True")
    assert LLMSettings().stream is True

    monkeypatch.setenv("LLM_STREAM", "False")
    assert LLMSettings().stream is False
