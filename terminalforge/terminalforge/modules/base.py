from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from terminalforge.core.models import ExecutionMode

@dataclass(frozen=True)
class ModuleInfo:
    id: str
    name: str
    description: str
    category: str
    ai_capable: bool = True

class ForgeModule:
    info: ModuleInfo

    def run_native(self, **_: Any) -> str:
        """Deterministic/local operation. Must work with no AI configured."""
        return f"{self.info.name}: native operation ready"

    def run(self, mode: ExecutionMode = ExecutionMode.NATIVE, **kwargs: Any) -> str:
        # The registry/UI can call this uniformly. AI orchestration lives above modules.
        return self.run_native(**kwargs)
