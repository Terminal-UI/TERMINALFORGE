# TerminalForge

> **The unified terminal workspace for developers, DevOps, cloud and AI.**

TerminalForge is a modular Python TUI/CLI designed around a single workspace for code, Git, containers, Kubernetes, cloud, databases, APIs, systems, networking, logs, security and agentic AI.

## Agentic AI

The `MindForge` subsystem supports **LangChain, LangGraph and CrewAI** through a common adapter boundary. This lets TerminalForge choose the right orchestration style without coupling the core application to one framework.

- LangChain: agents, tools and provider-neutral model interfaces.
- LangGraph: stateful graphs, persistence/HITL-ready orchestration and long-running workflows.
- CrewAI: role-based multi-agent Crews and event-driven Flows.
- Optional LangSmith integration is available for observability.

The design follows the current framework guidance: LangChain for standard agent applications, LangGraph for advanced orchestration, and CrewAI for collaborative agent teams and Flows.

## Modules

```text
terminalforge
├── code        → CodeForge
├── ai          → MindForge
├── git         → GitForge
├── docker      → ContainerForge
├── kubernetes  → KubeForge
├── cloud       → CloudForge
├── database    → DataForge
├── api         → ApiForge
├── system      → SysForge
├── network     → NetForge
├── logs        → LogForge
└── security    → SecureForge
```

## Install

Recommended with `uv`:

```bash
uv venv
source .venv/bin/activate
uv pip install -e '.[all,dev]'
```

Minimal TUI/CLI installation:

```bash
pip install -e .
```

## Configure AI accounts

You can add an account profile either with a key immediately or by setting it later.

```bash
tf account add openai work --model gpt-5.4
# or set it immediately on the fly
tf account add openai work --model gpt-5.4 --api-key "sk-..." --set-env

tf account add anthropic work --model claude-sonnet-4-6 --api-key "..." --set-env
tf account add deepseek lab --model deepseek-chat --api-key "..." --set-env
tf account add kimi lab --model moonshot-v1-8k --api-key "..." --set-env
tf account add google personal --model gemini-2.5-flash --api-key "..." --set-env

tf account list
```

If you do not pass `--api-key`, the command will prompt for the key interactively.

The generated environment variable name is based on the provider and account name, for example:

```bash
export TERMINALFORGE_OPENAI_WORK="..."
export TERMINALFORGE_ANTHROPIC_WORK="..."
export TERMINALFORGE_DEEPSEEK_LAB="..."
export TERMINALFORGE_KIMI_LAB="..."
export TERMINALFORGE_GOOGLE_PERSONAL="..."
```

You can also override the variable name explicitly:

```bash
tf account add google personal --model gemini-2.5-flash --api-key "..." --set-env --env-name GOOGLE_API_KEY
```

The key is stored locally in the TerminalForge secret store and can also be exported to the current shell session using `--set-env`.

Never put API keys in Git, `config.json`, shell scripts committed to the repository, or source code.

## Agent commands

```bash
tf agent frameworks

tf agent run \
  --framework langchain \
  --account openai/work \
  "Review the current repository architecture"

tf agent run \
  --framework langgraph \
  --account openai/work \
  "Design a safe Kubernetes deployment workflow"

tf agent run \
  --framework crewai \
  --account openai/work \
  "Have multiple engineering roles review this architecture"
```

## Architecture

See [`docs/architecture.md`](docs/architecture.md) and [`docs/agentic-architecture.md`](docs/agentic-architecture.md).

### Important design principle

TerminalForge does **not** expose arbitrary shell execution to an LLM by default. Future DevOps agents should use explicit tools with validation, allowlists, dry-runs, approvals, timeouts and audit logs.

## Development

```bash
pytest
ruff check .
```
