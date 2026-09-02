from __future__ import annotations
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, ListItem, ListView, Static
from terminalforge.agents.models import AgentFramework, AgentTask
from terminalforge.agents.service import AgentService
from terminalforge.core.config import ConfigStore
from terminalforge.core.models import ExecutionMode
from terminalforge.core.registry import ModuleRegistry


class TerminalForgeApp(App):
    TITLE = "TERMINALFORGE"
    CSS = """
    Screen { background: #0b1020; color: #e2e8f0; }
    #main { width: 100%; height: 100%; }
    #topbar { width: 100%; height: auto; background: #111827; color: #f8fafc; border-bottom: heavy #22c55e; padding: 0 2; }
    #layout { width: 100%; height: 1fr; }
    #sidebar { width: 34%; min-width: 25; max-width: 45; border: round #f59e0b; padding: 1; background: #111827; }
    #content { width: 66%; border: round #f59e0b; padding: 1; background: #0f172a; }
    #statusbar { height: auto; color: #dbeafe; background: #0b1220; padding: 0 1; margin-bottom: 1; }
    #taskbar { height: 3; color: #f8fafc; background: #172033; padding: 0 1; margin-bottom: 1; }
    #output { height: 1fr; padding: 1 1; background: #0b1220; border: round #1d4ed8; }
    #meta { height: auto; min-height: 7; padding: 1; margin-bottom: 1; background: #111827; border: round #334155; }
    ListView { height: 1fr; }
    ListView > ListItem { padding: 0 1; background: #111827; }
    ListView > ListItem--highlighted { background: #1d4ed8; color: #f8fafc; text-style: bold; }
    ListView > ListItem--highlighted Static { color: #f8fafc; }
    Input { margin-top: 1; background: #0b1220; color: #f8fafc; border: round #38bdf8; }
    .label { color: #fbbf24; text-style: bold; }
    .mode-pill { width: auto; padding: 0 1; margin-right: 1; color: #0b1020; text-style: bold; }
    .pill-ai { background: #34d399; }
    .pill-hybrid { background: #fbbf24; }
    .pill-native { background: #7dd3fc; }
    .hint { color: #cbd5e1; }
    Static { transition: background 150ms linear, color 150ms linear; }
    """
    BINDINGS = [("a", "toggle_mode", "Toggle AI"), ("p", "focus_prompt", "Prompt"), ("ctrl+p", "focus_prompt", "Prompt"), ("q", "quit", "Quit")]

    def __init__(self, registry: ModuleRegistry, config: ConfigStore):
        super().__init__()
        self.registry = registry
        self.config = config
        self.mode = config.load_mode()
        if self.mode == ExecutionMode.NATIVE and config.load_accounts():
            self.mode = ExecutionMode.AI
            self.config.save_mode(self.mode)

    def compose(self) -> ComposeResult:
        with Vertical(id="main"):
            yield Static(self._header_content(), id="topbar")
            with Horizontal(id="layout"):
                with Vertical(id="sidebar"):
                    yield Static("Modules", classes="label")
                    yield ListView(*[
                        ListItem(Static(f"{i}. {m.info.name:<18} — {m.info.description}"), id=m.info.id, classes="module-item")
                        for i, m in enumerate(self.registry.all(), 1)
                    ], id="modules")
                with Vertical(id="content"):
                    yield Static(self._banner(), id="banner")
                    yield Static(self._status_message(), id="statusbar")
                    yield Static(self._task_summary(), id="taskbar")
                    yield Static(self._default_metadata(), id="meta")
                    yield Static(self._default_dashboard(), id="output")
                    yield Input(placeholder="Ask the AI assistant... Press Enter to send", id="prompt")
            yield Static(self._footer_hint(), classes="hint")
        self.query_one("#prompt", Input).focus()

    def _header_content(self) -> str:
        status = self.mode.value.upper()
        return (
            f"[bold #f8fafc]TERMINALFORGE[/bold #f8fafc]   "
            f"[bold #7dd3fc]PROJECT[/bold #7dd3fc]: terminalforge   "
            f"[bold #a7f3d0]MODE[/bold #a7f3d0]: {status}   "
            f"[bold #fbbf24]STATE[/bold #fbbf24]: READY"
        )

    def _banner(self) -> str:
        return f"TERMINALFORGE\nDeveloper • Cloud • AI • Infrastructure\nExecution mode: {self.mode.value.upper()}"

    def _mode_pill(self) -> str:
        if self.mode == ExecutionMode.AI:
            return "[bold #0b1020] AI [/bold #0b1020]"
        if self.mode == ExecutionMode.HYBRID:
            return "[bold #0b1020] HYBRID [/bold #0b1020]"
        return "[bold #0b1020] NATIVE [/bold #0b1020]"

    def _status_message(self) -> str:
        if self.mode == ExecutionMode.AI:
            return f"{self._mode_pill()} • Agent workflows enabled • Ready for prompts"
        if self.mode == ExecutionMode.HYBRID:
            return f"{self._mode_pill()} • Local tools + AI review enabled"
        return f"{self._mode_pill()} • Deterministic workflows enabled"

    def _task_summary(self) -> str:
        return f"Active task: ready • project: terminalforge • mode: {self.mode.value.upper()}"

    def _default_dashboard(self) -> str:
        return (
            "Workspace overview\n"
            "- Select a module to inspect or execute it\n"
            "- Use the prompt box to send an AI task\n"
            "- [a] toggles execution mode, [p] focuses the prompt, [q] quits"
        )

    def _default_metadata(self) -> str:
        return (
            "Selected module metadata\n"
            "Name: none\n"
            "Focus: choose a module from the left to inspect its purpose and execution path"
        )

    def _module_summary(self, module: object) -> str:
        info = getattr(module, "info")
        return (
            f"Module: {info.name}\n"
            f"Description: {info.description}\n\n"
            f"Execution: {self.mode.value.upper()}\n"
            f"Status: ready\n"
            f"Summary: This TerminalForge module is designed to help accelerate developer workflows with focused operational tooling."
        )

    def _footer_hint(self) -> str:
        return "[a] Toggle Native/AI/Hybrid   [p] Prompt   [Enter] Open or run module   [q] Quit"

    def refresh_content(self) -> None:
        self.query_one("#topbar", Static).update(self._header_content())
        self.query_one("#banner", Static).update(self._banner())
        self.query_one("#statusbar", Static).update(self._status_message())
        self.query_one("#taskbar", Static).update(self._task_summary())
        self.query_one("#meta", Static).update(self._default_metadata())
        self.query_one("#output", Static).update(self._default_dashboard())

    def action_focus_prompt(self) -> None:
        self.query_one("#prompt", Input).focus()

    def action_toggle_mode(self) -> None:
        order = [ExecutionMode.NATIVE, ExecutionMode.HYBRID, ExecutionMode.AI]
        self.mode = order[(order.index(self.mode) + 1) % len(order)]
        self.config.save_mode(self.mode)
        self.refresh_content()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        module = self.registry.get(event.item.id)
        if not module:
            return

        info = getattr(module, "info")
        selected = (
            f"Selected module metadata\n"
            f"Name: {info.name}\n"
            f"Description: {info.description}\n"
            f"Execution mode: {self.mode.value.upper()}\n"
            f"Status: ready"
        )
        self.query_one("#meta", Static).update(selected)
        summary = self._module_summary(module)
        if self.mode == ExecutionMode.AI:
            prompt = self._agent_prompt_for(module)
            try:
                result = AgentService().run(AgentTask(objective=prompt, framework=AgentFramework.LANGCHAIN, account=None))
                self.query_one("#output", Static).update(f"{summary}\n\nAI Analysis:\n{result.output}")
                return
            except RuntimeError:
                self.query_one("#output", Static).update(
                    f"{summary}\n\nAI mode: no configured account was found. Add one with `tf account add ...` first.\n\nNative fallback:\n{module.run_native()}"
                )
                return

        message = module.run_native()
        if self.mode == ExecutionMode.HYBRID:
            message += "\n\nHybrid mode: deterministic execution is active; AI can be used for planning/review."
        self.query_one("#output", Static).update(f"{summary}\n\nModule output:\n{message}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "prompt":
            return
        text = event.value.strip()
        if not text:
            return
        try:
            result = AgentService().run(AgentTask(objective=text, framework=AgentFramework.LANGCHAIN, account=None))
            self.query_one("#output", Static).update(
                f"Prompt dispatched\nRequest: {text}\n\nAgent response:\n{result.output}"
            )
        except RuntimeError:
            self.query_one("#output", Static).update(
                f"Prompt dispatched\nRequest: {text}\n\nAI mode: no configured account was found. Add one with `tf account add ...` first."
            )
        event.input.value = ""

    @staticmethod
    def _agent_prompt_for(module: object) -> str:
        info = getattr(module, "info")
        return (
            f"Review the TerminalForge module '{info.name}' and explain what it does in the context of this project. "
            f"Use the module description: '{info.description}'. Provide a concise but practical summary and any risks or next steps."
        )
