# Architecture and research notes

## TUI choice

TerminalForge uses **Textual** initially because it gives Python a high-level reactive TUI model and integrates with Rich. The core application is intentionally separated from rendering so the UI can be replaced or supplemented later.

Two strong alternatives were reviewed:

- **OpenTUI:** native Zig terminal renderer with TypeScript bindings, Flexbox layout, and React/Solid options. It is particularly interesting for a future TypeScript frontend.
- **Ratatui:** Rust TUI framework with a lightweight widget model and Crossterm backend; a good future high-performance frontend.

## AI provider design

Providers expose a common `chat()` contract. OpenAI, DeepSeek, and Kimi are particularly easy to normalize because their APIs expose OpenAI-compatible formats. Anthropic has its own API shape, and Google Gemini has its own SDK/API model, so adapters remain provider-specific behind one interface.

## Account groups

An account is a named profile, not a password vault. Example groups:

- `google/personal`
- `google/work`
- `openai/work`
- `anthropic/personal`
- `deepseek/lab`
- `kimi/lab`

Only secret references and non-sensitive metadata should be persisted. The starter supports environment-variable secret resolution and a permissions-restricted local secret store fallback. Production deployments should prefer an OS/cloud secret manager.

## Module contract

Every module implements a small `ForgeModule` protocol with an id, display name, description, and `run()` entry point. This makes new modules independently testable and avoids a monolithic application class.
