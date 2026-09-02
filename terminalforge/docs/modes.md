# TerminalForge: Native + AI modes

TerminalForge is designed as a **dual-mode workspace**:

- **Native mode**: no AI SDKs, no AI account, no API key. Deterministic CLI/TUI tooling works locally.
- **AI mode**: optional LangChain/LangGraph/CrewAI orchestration with configured provider accounts.
- **Hybrid mode**: deterministic tools remain the source of truth; AI can plan, explain, review, or propose actions before execution.

The core application must never import an optional AI framework at startup. AI adapters lazy-import their framework dependencies and fail with an actionable installation message.

Recommended progression:

```text
Native -> Hybrid -> AI
   |         |       |
   |         |       +-- autonomous/agentic workflows
   |         +---------- AI-assisted planning/review
   +-------------------- deterministic developer/DevOps tools
```

For production, tool execution should pass through a policy/approval layer before mutating infrastructure.
