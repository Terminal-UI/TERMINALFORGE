from __future__ import annotations
from terminalforge.core.models import ExecutionMode

class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, object] = {}
    def register(self, module: object) -> None:
        self._modules[module.info.id] = module
    def all(self, mode: ExecutionMode | None = None) -> list[object]:
        modules = list(self._modules.values())
        if mode == ExecutionMode.AI:
            modules = [m for m in modules if getattr(m.info, "ai_capable", False)]
        return modules
    def get(self, module_id: str) -> object | None:
        return self._modules.get(module_id)
