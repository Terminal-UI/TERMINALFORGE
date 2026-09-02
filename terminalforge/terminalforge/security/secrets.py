from __future__ import annotations
import os
from pathlib import Path
from platformdirs import user_config_dir

class SecretStore:
    """Minimal secret resolver. Prefer an OS keyring/cloud secret manager in production."""
    def get(self, ref: str | None) -> str | None:
        if not ref: return None
        value = os.getenv(ref)
        if value: return value
        fallback = Path(user_config_dir("terminalforge")) / "secrets" / ref
        if fallback.exists(): return fallback.read_text().strip()
        return None
    def set_local(self, ref: str, value: str) -> None:
        folder = Path(user_config_dir("terminalforge")) / "secrets"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / ref
        path.write_text(value)
        path.chmod(0o600)
