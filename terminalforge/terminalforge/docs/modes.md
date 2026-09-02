# Native, Hybrid and AI execution

## Native

Native mode is a complete first-class product mode. It must remain usable on a machine with no AI libraries and no AI account. Forge modules execute deterministic/local operations and expose safe command/tool boundaries.

## AI

AI mode adds optional agent runtimes. LangChain is used for general tool-using agents, LangGraph for explicit stateful workflows, and CrewAI for collaborative agent teams. The framework layer is an adapter boundary so the rest of TerminalForge does not depend on one runtime.

## Hybrid

Hybrid mode is the recommended operational model. An AI agent can inspect context, propose a plan and review results, while deterministic Forge modules remain the source of truth for execution. Destructive operations should pass through a policy and human-approval gate.

## Design rule

AI must be an accelerator, never a hidden requirement for the underlying developer/DevOps functionality.
