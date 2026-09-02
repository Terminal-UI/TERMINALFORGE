from __future__ import annotations
import json
from pathlib import Path
from platformdirs import user_config_dir
from terminalforge.core.models import AccountProfile, ExecutionMode

class ConfigStore:
    def __init__(self, path: Path | None = None, mode_path: Path | None = None) -> None:
        base = Path(user_config_dir("terminalforge"))
        self.path = path or base / "accounts.json"
        self.mode_path = mode_path or base / "mode.json"

    def load_accounts(self) -> list[AccountProfile]:
        if not self.path.exists():
            return []
        return [AccountProfile.model_validate(x) for x in json.loads(self.path.read_text())]

    def save_accounts(self, accounts: list[AccountProfile]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([a.model_dump(mode="json") for a in accounts], indent=2))
        self.path.chmod(0o600)

    def load_mode(self) -> ExecutionMode:
        if not self.mode_path.exists():
            return ExecutionMode.NATIVE
        return ExecutionMode(json.loads(self.mode_path.read_text()).get("mode", "native"))

    def save_mode(self, mode: ExecutionMode) -> None:
        self.mode_path.parent.mkdir(parents=True, exist_ok=True)
        self.mode_path.write_text(json.dumps({"mode": mode.value}, indent=2))
        self.mode_path.chmod(0o600)
