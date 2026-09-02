from terminalforge.agents.models import AgentFramework, AgentTask
from terminalforge.agents.service import AgentService


def test_agent_frameworks_are_registered_without_optional_dependencies():
    service = AgentService()
    assert service.frameworks() == ["langchain", "langgraph", "crewai"]


def test_agent_task_defaults():
    task = AgentTask(objective="test")
    assert task.framework == AgentFramework.LANGCHAIN
    assert task.max_steps == 8
