# Product modes

TerminalForge is one product with three execution profiles rather than two separate codebases.

### Native / No AI

```text
User -> TUI/CLI -> Forge Module -> Local/Cloud Tool
```

No LLM calls, no agent runtime, no AI credentials. This is the deterministic developer/DevOps workstation.

### AI

```text
User -> Agent Runtime -> AI Tool Registry -> Forge Module -> Tool
                     \-> LLM Provider
```

LangChain, LangGraph or CrewAI can reason over the task and invoke governed tools. AI credentials are isolated in account profiles.

### Hybrid

```text
User -> AI Planner -> Proposed Plan -> Approval -> Forge Module -> Tool
                    \-> Review/Explain
```

This is the preferred production mode for infrastructure changes because the deterministic Forge layer remains authoritative.

The critical rule is: **AI is optional at install time and optional at runtime. The core product never depends on an LLM.**
