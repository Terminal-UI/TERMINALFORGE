from terminalforge.core.config import ConfigStore
from terminalforge.core.models import ExecutionMode
from terminalforge.core.registry import ModuleRegistry
from terminalforge.modules.code import CodeForge


def test_native_is_default_and_persistent(tmp_path):
    cfg = ConfigStore(tmp_path / "accounts.json", tmp_path / "mode.json")
    assert cfg.load_mode() == ExecutionMode.NATIVE
    cfg.save_mode(ExecutionMode.AI)
    assert cfg.load_mode() == ExecutionMode.AI


def test_registry_works_without_ai_runtime():
    registry = ModuleRegistry()
    registry.register(CodeForge())
    assert registry.get("code").run_native() == "CodeForge: native operation ready"
