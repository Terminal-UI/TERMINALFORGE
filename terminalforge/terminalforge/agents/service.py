from __future__ import annotations
from terminalforge.agents.models import AgentFramework, AgentResult, AgentTask
from terminalforge.core.config import ConfigStore
from terminalforge.security.secrets import SecretStore
from terminalforge.core.models import Provider, AccountProfile
from .frameworks import CrewAIAdapter, LangChainAdapter, LangGraphAdapter

class AgentService:
    """Optional agentic layer. Core/native TerminalForge never requires AI packages."""
    def __init__(self, config: ConfigStore | None = None, secrets: SecretStore | None = None):
        self.config = config or ConfigStore()
        self.secrets = secrets or SecretStore()
        self.adapters = {
            AgentFramework.LANGCHAIN: LangChainAdapter(),
            AgentFramework.LANGGRAPH: LangGraphAdapter(),
            AgentFramework.CREWAI: CrewAIAdapter(),
        }

    def frameworks(self) -> list[str]:
        return [x.value for x in AgentFramework]

    def run(self, task: AgentTask) -> AgentResult:
        account = self._account(task.account)
        key = self.secrets.get(account.secret_ref) if account.secret_ref else None
        if not key:
            raise RuntimeError(f"No API credential available for {account.group}/{account.provider}/{account.name}")
        model = account.model or self._default_model(account.provider)
        return self.adapters[task.framework].run(
            task, provider=account.provider, model=model, api_key=key, base_url=self._base_url(account)
        )

    def _account(self, ref: str | None) -> AccountProfile:
        accounts = [a for a in self.config.load_accounts() if a.enabled]
        if not accounts:
            raise RuntimeError("No AI accounts configured. Use `tf account add ...` first.")
        if not ref:
            return accounts[0]
        parts = ref.split("/")
        if len(parts) == 3:
            group, provider, name = parts
            for account in accounts:
                if account.group == group and account.provider.value == provider and account.name == name:
                    return account
        elif len(parts) == 2:  # backward-compatible provider/name
            provider, name = parts
            for account in accounts:
                if account.provider.value == provider and account.name == name:
                    return account
        raise ValueError(f"Unknown AI account: {ref}")

    @staticmethod
    def _default_model(provider: Provider) -> str:
        return {
            Provider.OPENAI: "gpt-5.4",
            Provider.ANTHROPIC: "claude-sonnet-4-6",
            Provider.DEEPSEEK: "deepseek-chat",
            Provider.KIMI: "moonshot-v1-8k",
            Provider.GOOGLE: "gemini-2.5-flash",
        }[provider]

    @staticmethod
    def _base_url(account: AccountProfile) -> str | None:
        return {Provider.DEEPSEEK: "https://api.deepseek.com", Provider.KIMI: "https://api.moonshot.ai/v1"}.get(account.provider)
