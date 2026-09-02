from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field

class AgentFramework(StrEnum):
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"

class AgentTask(BaseModel):
    objective: str
    context: str = ""
    framework: AgentFramework = AgentFramework.LANGCHAIN
    account: str | None = None
    max_steps: int = Field(default=8, ge=1, le=100)
    execute_tools: bool = False

class AgentResult(BaseModel):
    output: str
    framework: AgentFramework
    model: str = "unknown"
    tool_calls: list[str] = Field(default_factory=list)
    steps: int = 0
