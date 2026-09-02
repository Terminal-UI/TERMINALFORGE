from __future__ import annotations
from terminalforge.agents.models import AgentResult, AgentTask
from terminalforge.core.models import Provider
from .base import AgentFrameworkAdapter
from .model_factory import build_chat_model

class LangChainAdapter(AgentFrameworkAdapter):
    name = "langchain"
    def run(self, task: AgentTask, *, provider: Provider, model: str, api_key: str, base_url: str | None = None) -> AgentResult:
        try:
            from langchain.agents import create_agent
            from langchain_core.tools import tool
        except ImportError as exc:
            raise RuntimeError("LangChain is not installed. Run: pip install 'terminalforge[agentic]'") from exc
        llm = build_chat_model(provider, model, api_key, base_url)
        @tool
        def terminal_context() -> str:
            """Return safe static context describing the TerminalForge workspace."""
            return "TerminalForge is a developer, DevOps and AI terminal workspace."
        agent = create_agent(model=llm, tools=[terminal_context], system_prompt="You are TerminalForge Agent. Be safe and precise.")
        prompt = task.objective if not task.context else f"{task.objective}\nContext:\n{task.context}"
        result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        messages = result.get("messages", [])
        content = messages[-1].content if messages else ""
        if isinstance(content, list):
            content = "".join(str(x.get("text", x)) if isinstance(x, dict) else str(x) for x in content)
        return AgentResult(output=str(content), framework=task.framework, model=model, steps=len(messages))
