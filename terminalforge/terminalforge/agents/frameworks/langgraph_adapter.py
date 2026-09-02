from __future__ import annotations
from typing import TypedDict
from terminalforge.agents.models import AgentResult, AgentTask
from terminalforge.core.models import Provider
from .base import AgentFrameworkAdapter
from .model_factory import build_chat_model

class _State(TypedDict):
    prompt: str
    output: str

class LangGraphAdapter(AgentFrameworkAdapter):
    name = "langgraph"
    def run(self, task: AgentTask, *, provider: Provider, model: str, api_key: str, base_url: str | None = None) -> AgentResult:
        try:
            from langchain.agents import create_agent
            from langgraph.graph import END, START, StateGraph
        except ImportError as exc:
            raise RuntimeError("LangGraph/LangChain is not installed. Run: pip install 'terminalforge[agentic]'") from exc
        llm = build_chat_model(provider, model, api_key, base_url)
        agent = create_agent(model=llm, tools=[], system_prompt="You are a TerminalForge planning agent.")
        def execute(state: _State) -> dict[str, str]:
            result = agent.invoke({"messages": [{"role": "user", "content": state["prompt"]}]})
            content = result["messages"][-1].content
            if isinstance(content, list):
                content = "".join(str(x.get("text", x)) if isinstance(x, dict) else str(x) for x in content)
            return {"output": str(content)}
        graph = StateGraph(_State)
        graph.add_node("execute", execute); graph.add_edge(START, "execute"); graph.add_edge("execute", END)
        result = graph.compile().invoke({"prompt": task.objective if not task.context else f"{task.objective}\nContext:\n{task.context}", "output": ""})
        return AgentResult(output=result["output"], framework=task.framework, model=model, steps=1)
