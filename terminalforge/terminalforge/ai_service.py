from __future__ import annotations
from terminalforge.core.config import ConfigStore
from terminalforge.core.models import AccountProfile
from terminalforge.providers.base import ChatRequest
from terminalforge.providers.factory import provider_for
from terminalforge.security.secrets import SecretStore

class AIService:
    def __init__(self, config: ConfigStore | None = None, secrets: SecretStore | None = None):
        self.config = config or ConfigStore(); self.secrets = secrets or SecretStore()
    def accounts(self) -> list[AccountProfile]: return self.config.load_accounts()
    def chat(self, account: AccountProfile, prompt: str) -> str:
        key = self.secrets.get(account.secret_ref)
        if not key: raise RuntimeError(f"No secret available for {account.provider}/{account.name}")
        model = account.model or {"openai":"gpt-5","anthropic":"claude-sonnet-4-5","deepseek":"deepseek-v4-flash","kimi":"kimi-k3","google":"gemini-2.5-flash"}[account.provider.value]
        return provider_for(account.provider).chat(ChatRequest(model=model, prompt=prompt), key)
