
from myagent.core.config import LLMSettings, Settings, ToolsSettings

LLM_ENV_KEYS = (
    "LLM_MODEL",
    "LLM_BASE_URL",
    "LLM_API_KEY",
    "LLM_STREAM",
    "LLM_REASONING_EFFORT",
    "LLM_THINKING_TYPE",
)

TOOLS_ENV_KEYS = (
    "TOOLS_WEB_SEARCH_API_KEY",
    "TOOLS_CTX7_API_KEY",
    "TOOLS_WEB_SEARCH_ENGINE",
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


def test_tools_settings_defaults(monkeypatch):
    for key in TOOLS_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    settings = ToolsSettings(_env_file=None)

    assert settings.web_search_api_key == "YOUR_SEARCH_API_KEY_HERE"
    assert settings.ctx7_api_key == "YOUR_CTX7_API_KEY_HERE"


def test_env_prefix_is_isolated(monkeypatch):
    monkeypatch.setenv("TOOLS_WEB_SEARCH_API_KEY", "tvly-from-env")
    monkeypatch.setenv("LLM_API_KEY", "sk-from-env")

    assert ToolsSettings().web_search_api_key == "tvly-from-env"
    assert LLMSettings().api_key == "sk-from-env"
    # 每个分组只读自己的前缀，互不串台
    assert ToolsSettings().web_search_api_key != LLMSettings().api_key


def test_settings_aggregates_groups(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "deepseek-flash")
    monkeypatch.setenv("TOOLS_WEB_SEARCH_API_KEY", "tvly-xxx")

    settings = Settings()

    assert settings.llm.model == "deepseek-flash"
    assert settings.tools.web_search_api_key == "tvly-xxx"


def test_bool_parsing(monkeypatch):
    monkeypatch.setenv("LLM_STREAM", "True")
    assert LLMSettings().stream is True

    monkeypatch.setenv("LLM_STREAM", "False")
    assert LLMSettings().stream is False
