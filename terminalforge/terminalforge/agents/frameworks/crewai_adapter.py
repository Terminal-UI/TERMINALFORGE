from __future__ import annotations
import os
from terminalforge.agents.models import AgentResult, AgentTask
from terminalforge.core.models import Provider
from .base import AgentFrameworkAdapter

class CrewAIAdapter(AgentFrameworkAdapter):
    name = "crewai"
    def run(self, task: AgentTask, *, provider: Provider, model: str, api_key: str, base_url: str | None = None) -> AgentResult:
        try:
            from crewai import Agent, Crew, Task
        except ImportError as exc:
            raise RuntimeError("CrewAI is not installed. Run: pip install 'terminalforge[agentic]'") from exc
        env_name = {Provider.OPENAI: "OPENAI_API_KEY", Provider.ANTHROPIC: "ANTHROPIC_API_KEY", Provider.GOOGLE: "GEMINI_API_KEY", Provider.DEEPSEEK: "OPENAI_API_KEY", Provider.KIMI: "OPENAI_API_KEY"}[provider]
        os.environ[env_name] = api_key
        if base_url: os.environ["OPENAI_BASE_URL"] = base_url
        llm_name = {Provider.OPENAI: f"openai/{model}", Provider.ANTHROPIC: f"anthropic/{model}", Provider.GOOGLE: f"gemini/{model}", Provider.DEEPSEEK: f"openai/{model}", Provider.KIMI: f"openai/{model}"}[provider]
        agent = Agent(role="TerminalForge Agent", goal="Complete the technical objective safely.", backstory="Experienced developer and DevOps engineer.", llm=llm_name, verbose=False, allow_delegation=False)
        prompt = task.objective if not task.context else f"{task.objective}\nContext:\n{task.context}"
        result = Crew(agents=[agent], tasks=[Task(description=prompt, expected_output="A concise actionable response.", agent=agent)], verbose=False).kickoff()
        return AgentResult(output=str(result), framework=task.framework, model=model, steps=1)
