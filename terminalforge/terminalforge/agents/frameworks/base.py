from __future__ import annotations
from abc import ABC, abstractmethod
from terminalforge.agents.models import AgentResult, AgentTask
from terminalforge.core.models import Provider

class AgentFrameworkAdapter(ABC):
    name: str

    @abstractmethod
    def run(self, task: AgentTask, *, provider: Provider, model: str, api_key: str, base_url: str | None = None) -> AgentResult:
        raise NotImplementedError
