from terminalforge.core.models import Provider
from terminalforge.providers.anthropic import AnthropicProvider
from terminalforge.providers.google import GoogleProvider
from terminalforge.providers.openai_compat import OpenAICompatibleProvider

def provider_for(provider: Provider):
    return {
        Provider.OPENAI: lambda: OpenAICompatibleProvider("openai", "https://api.openai.com/v1"),
        Provider.DEEPSEEK: lambda: OpenAICompatibleProvider("deepseek", "https://api.deepseek.com"),
        Provider.KIMI: lambda: OpenAICompatibleProvider("kimi", "https://api.moonshot.ai/v1"),
        Provider.ANTHROPIC: AnthropicProvider,
        Provider.GOOGLE: GoogleProvider,
    }[provider]()
