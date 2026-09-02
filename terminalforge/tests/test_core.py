from typer.testing import CliRunner

from terminalforge.cli import app
from terminalforge.core.config import ConfigStore
from terminalforge.core.models import AccountProfile, ExecutionMode, Provider
from terminalforge.modules.code import CodeForge
from terminalforge.ui.app import TerminalForgeApp


def test_account_roundtrip(tmp_path):
    s = ConfigStore(tmp_path / 'accounts.json')
    s.save_accounts([AccountProfile(provider=Provider.GOOGLE, name='work', group='engineering', model='gemini-2.5-flash', secret_ref='X')])
    a = s.load_accounts()[0]
    assert a.provider == Provider.GOOGLE and a.name == 'work' and a.group == 'engineering'


def test_account_add_accepts_api_key_and_prints_export():
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            'account', 'add', 'openai', 'work',
            '--model', 'gpt-5.4',
            '--api-key', 'sk-test-123',
            '--set-env',
        ],
    )
    assert result.exit_code == 0, result.output
    assert 'TERMINALFORGE_OPENAI_WORK' in result.output
    assert 'sk-test-123' in result.output


def test_ai_selection_uses_agent_prompt_for_module():
    app = TerminalForgeApp(type('R', (), {'all': lambda self, mode=None: [CodeForge()]})(), ConfigStore())
    app.mode = ExecutionMode.AI
    prompt = app._agent_prompt_for(CodeForge())
    assert 'CodeForge' in prompt
    assert 'module description' in prompt.lower() or 'CodeForge' in prompt


def test_app_defaults_to_ai_when_account_exists(tmp_path):
    cfg = ConfigStore(tmp_path / 'accounts.json', tmp_path / 'mode.json')
    cfg.save_accounts([AccountProfile(provider=Provider.OPENAI, name='work', group='default', model='gpt-5.4', secret_ref='X')])
    app = TerminalForgeApp(type('R', (), {'all': lambda self, mode=None: [CodeForge()]})(), cfg)
    assert app.mode == ExecutionMode.AI


def test_app_has_prompt_shortcode_and_prompt_field():
    app = TerminalForgeApp(type('R', (), {'all': lambda self, mode=None: [CodeForge()]})(), ConfigStore())
    assert any(binding[0] in {'p', 'ctrl+p'} for binding in app.BINDINGS)
    assert hasattr(app, 'action_focus_prompt')


def test_app_builds_richer_module_summary():
    app = TerminalForgeApp(type('R', (), {'all': lambda self, mode=None: [CodeForge()]})(), ConfigStore())
    summary = app._module_summary(CodeForge())
    assert 'CodeForge' in summary
    assert 'module' in summary.lower()
