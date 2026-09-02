from __future__ import annotations
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Static, ListItem, ListView
from textual.screen import ModalScreen
from terminalforge.core.registry import ModuleRegistry
from terminalforge.core.config import ConfigStore
from terminalforge.core.models import ExecutionMode

class TerminalForgeApp(App):
    TITLE = "TERMINALFORGE"
    CSS = """
    Screen { align: center middle; }
    #main { width: 86%; height: 86%; border: round $accent; padding: 1 2; }
    ListView { height: 1fr; }
    .hint { margin: 1; }
    """
    BINDINGS = [("a", "toggle_mode", "Toggle AI"), ("q", "quit", "Quit")]

    def __init__(self, registry: ModuleRegistry, config: ConfigStore):
        super().__init__(); self.registry = registry; self.config = config
        self.mode = config.load_mode()

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main"):
            yield Static(self._banner(), id="banner", classes="hint")
            yield ListView(*[ListItem(Static(f"{i}. {m.info.name:<18} — {m.info.description}"), id=m.info.id)
                             for i, m in enumerate(self.registry.all(), 1)], id="modules")
            yield Static("[a] Toggle Native/AI/Hybrid   [Enter] Open module   [q] Quit", classes="hint")
        yield Footer()

    def _banner(self) -> str:
        return f"TERMINALFORGE\nDeveloper • Cloud • AI • Infrastructure\nExecution mode: {self.mode.value.upper()}"

    def action_toggle_mode(self) -> None:
        order = [ExecutionMode.NATIVE, ExecutionMode.HYBRID, ExecutionMode.AI]
        self.mode = order[(order.index(self.mode) + 1) % len(order)]
        self.config.save_mode(self.mode)
        self.query_one("#banner", Static).update(self._banner())

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        module = self.registry.get(event.item.id)
        if module:
            message = module.run_native()
            if self.mode == ExecutionMode.AI:
                message += "\n\nAI mode: use `tf agent run` to delegate reasoning to a configured agent."
            elif self.mode == ExecutionMode.HYBRID:
                message += "\n\nHybrid mode: deterministic execution is active; AI can be used for planning/review."
            self.push_screen(ModuleScreen(module.info.name, message))

class ModuleScreen(ModalScreen):
    def __init__(self, title: str, message: str):
        super().__init__(); self.title_text = title; self.message = message
    def compose(self):
        yield Static(f"{self.title_text}\n\n{self.message}\n\nPress Esc to return.", id="main")
