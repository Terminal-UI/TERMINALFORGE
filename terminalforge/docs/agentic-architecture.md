# TerminalForge Agentic AI Architecture

TerminalForge uses a **framework-neutral agent boundary** and supports three complementary agentic runtimes:

- **LangChain** — high-level agent abstraction, standardized model/tool interfaces.
- **LangGraph** — explicit stateful orchestration for multi-step, durable workflows.
- **CrewAI** — role-based multi-agent collaboration through Crews and event-driven Flows.

This is intentionally not a "pick one forever" architecture. TerminalForge selects the right runtime per workload.

## Runtime selection

| Need | Runtime |
|---|---|
| Single agent + tools | LangChain |
| Stateful graph / approvals / long-running workflow | LangGraph |
| Multiple role-based agents collaborating | CrewAI |
| Deterministic + agentic hybrid | LangGraph wrapping LangChain agents |

LangChain's current `create_agent` implementation is graph-based and uses LangGraph underneath. LangGraph is the lower-level orchestration layer for durable execution, streaming, persistence and human-in-the-loop workflows. CrewAI provides a separate agent/crew/flow stack and does not depend on LangChain.

## Account model

Accounts are named profiles such as:

```text
google/personal
google/work
openai/personal
openai/work
anthropic/work
deepseek/lab
kimi/lab
```

Only an environment-variable reference is stored in the profile. API keys are never written to the JSON configuration.

## Safety boundary

The current agentic layer intentionally exposes **no unrestricted shell tool**. DevOps tools should be added through explicit, auditable adapters with:

1. allowlists
2. argument validation
3. dry-run support
4. approval gates for destructive actions
5. command timeout
6. audit events
7. least-privilege execution

This prevents an LLM from receiving arbitrary host access merely because TerminalForge is a terminal application.

## Example

```bash
tf account add openai work --model gpt-5.4
tf account add google personal --model gemini-2.5-flash
export TERMINALFORGE_OPENAI_WORK="$OPENAI_API_KEY"

tf agent run --framework langchain --account openai/work "Explain the current git repository architecture"
tf agent run --framework langgraph --account openai/work "Plan a safe Kubernetes deployment and identify approval points"
tf agent run --framework crewai --account openai/work "Have architect, security and DevOps agents review this deployment plan"
```
