"""应用配置。

按「前缀」分组：每个分组一个 BaseSettings 子类，通过 env_prefix 声明自己的
环境变量前缀，因此同一个 .env 文件里可以并存多组配置而互不干扰：

    LLM_MODEL / LLM_BASE_URL / LLM_API_KEY / ...
    WEB_SEARCH_ENGINE / WEB_SEARCH_API_KEY
    （新增分组只要继承 _PrefixedSettings 并起个新前缀）
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（src/myagent/core/config.py -> 上溯 4 层），用于定位 .env，
# 这样无论从哪个目录启动都能读到同一份配置。
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_FILE = _PROJECT_ROOT / ".env"
if not _ENV_FILE.is_file():
    # 装成 wheel 等场景下 __file__ 不在源码树里，退回当前工作目录
    _ENV_FILE = Path(".env")


def _config(prefix: str) -> SettingsConfigDict:
    """生成某个分组的 model_config：统一 .env 路径 + 该分组的前缀。"""
    return SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        env_prefix=prefix,
        case_sensitive=False,  # LLM_MODEL 与 llm_model 等价
        extra="ignore",        # .env 里属于其它分组的键全部忽略
    )


class _PrefixedSettings(BaseSettings):
    """所有分组配置的基类（只定义公共行为，本身不含字段）。"""

    model_config = _config("")


class LLMSettings(_PrefixedSettings):
    # 读取 LLM_MODEL / LLM_BASE_URL / LLM_API_KEY / LLM_STREAM / ...
    model_config = _config("LLM_")

    model: str = "deepseek-flash"
    base_url: str = "https://api.deepseek.com"
    api_key: str = "YOUR_API_KEY_HERE"
    stream: bool = False
    reasoning_effort: str = "high"
    thinking_type: str = "disabled"


class ToolsSettings(_PrefixedSettings):
    # 读取 TOOLS_CONFIG
    model_config = _config("TOOLS_")
    web_search_api_key: str = "YOUR_SEARCH_API_KEY_HERE"
    ctx7_api_key: str = "YOUR_CTX7_API_KEY_HERE"


class Settings(_PrefixedSettings):
    """全局配置对象，包含所有分组的配置。"""

    model_config = _config("")
    llm: LLMSettings = Field(default_factory=LLMSettings)
    tools: ToolsSettings = Field(default_factory=ToolsSettings)

@lru_cache
def get_settings() -> Settings:
    """返回全局配置对象（单例）。"""
    return Settings()
def get_llm_settings() -> LLMSettings:
    """返回 LLM 分组配置对象（单例）。"""
    return get_settings().llm
def get_tools_settings() -> ToolsSettings:
    """返回 Tools 分组配置对象（单例）。"""
    return get_settings().tools

