from __future__ import annotations
from terminalforge.core.models import Provider


def build_chat_model(provider: Provider, model: str, api_key: str, base_url: str | None = None):
    """Build a LangChain chat model for a TerminalForge provider account."""
    if provider == Provider.ANTHROPIC:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model, api_key=api_key, temperature=0)
    if provider == Provider.GOOGLE:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model, google_api_key=api_key, temperature=0)
    from langchain_openai import ChatOpenAI
    kwargs = {"model": model, "api_key": api_key, "temperature": 0}
    if base_url:
        kwargs["base_url"] = base_url
    return ChatOpenAI(**kwargs)
