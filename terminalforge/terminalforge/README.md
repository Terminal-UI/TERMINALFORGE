# TerminalForge

**The unified terminal workspace for developers, DevOps and AI — with or without AI.**

## Two product modes

TerminalForge is intentionally **AI-optional**:

| Mode | AI packages | API credentials | Use case |
|---|---|---|---|
| Native | Not required | Not required | Git, Docker, Kubernetes, cloud, DB, system, network, logs, security tools |
| Hybrid | Optional | Optional | deterministic tools + AI planning/review |
| AI | Required | Required | LangChain/LangGraph/CrewAI agentic workflows |

The base install never imports an AI SDK during startup. Agent frameworks are lazy-loaded only when an AI command is executed.

## Install

```bash
pip install -e .
```

AI-enabled installation:

```bash
pip install -e '.[agentic]'
```

Everything:

```bash
pip install -e '.[all,dev]'
```

## Run without AI

```bash
tf
# or
tf mode set native
tf module list
tf module run git
```

No AI account or API key is needed.

## Run with AI

```bash
tf mode set ai
tf account add openai work --group engineering --model gpt-5.4
```

Set the generated environment variable, then:

```bash
tf agent frameworks
tf agent run "Review this repository architecture" --framework langgraph --account engineering/openai/work
```

Supported providers: OpenAI, Anthropic, DeepSeek, Kimi and Google Gemini.

## Hybrid

```bash
tf mode set hybrid
```

Hybrid is the recommended production direction: deterministic Forge tools remain the source of truth while AI provides planning, explanation and review. Mutating operations should eventually pass through an approval/policy engine.

## Architecture

```text
                         TERMINALFORGE
                              |
              +---------------+---------------+
              |               |               |
           NATIVE           HYBRID            AI
              |               |               |
        Forge Modules     AI Planner      Agent Runtime
              |               |         +-----+-----+
       Git/Docker/K8s      Review       |     |     |
       Cloud/DB/System       |       LangChain LangGraph CrewAI
       Network/Logs/Sec      +--------------+-------------+
                              |
                        Provider Layer
                    OpenAI / Claude / Gemini
                    DeepSeek / Kimi
```

See `docs/modes.md` and `docs/agentic-architecture.md`.
