from __future__ import annotations
import os
import sys
import typer
from terminalforge.agents.models import AgentFramework, AgentTask
from terminalforge.agents.service import AgentService
from terminalforge.core.config import ConfigStore
from terminalforge.core.models import AccountProfile, Provider, ExecutionMode
from terminalforge.core.registry import ModuleRegistry
from terminalforge.modules import code, git, ai, docker, kubernetes, cloud, database, api, system, network, logs, security
from terminalforge.security.secrets import SecretStore

app = typer.Typer(no_args_is_help=False, add_completion=False)
account_app = typer.Typer(help="Manage named AI account profiles")
module_app = typer.Typer(help="Run a TerminalForge module")
agent_app = typer.Typer(help="Run optional agentic AI workflows")
mode_app = typer.Typer(help="Select native, AI, or hybrid execution")
app.add_typer(account_app, name="account")
app.add_typer(module_app, name="module")
app.add_typer(agent_app, name="agent")
app.add_typer(mode_app, name="mode")

def registry() -> ModuleRegistry:
    r = ModuleRegistry()
    for cls in [code.CodeForge, git.GitForge, ai.MindForge, docker.ContainerForge, kubernetes.KubeForge,
                cloud.CloudForge, database.DataForge, api.ApiForge, system.SysForge, network.NetForge,
                logs.LogForge, security.SecureForge]:
        r.register(cls())
    return r

@app.callback()
def main_callback():
    """TerminalForge unified terminal workspace — native first, AI optional."""

@mode_app.command("get")
def mode_get():
    typer.echo(ConfigStore().load_mode().value)

@mode_app.command("set")
def mode_set(mode: ExecutionMode):
    ConfigStore().save_mode(mode)
    typer.echo(f"Execution mode: {mode.value}")

@account_app.command("add")
def account_add(
    provider: Provider,
    name: str,
    model: str = "",
    label: str = "",
    group: str = "default",
    api_key: str = typer.Option("", "--api-key", "-k", help="API key to associate with this account immediately."),
    set_env: bool = typer.Option(False, "--set-env", help="Set the generated environment variable in the current process and also persist it locally."),
    env_name: str | None = typer.Option(None, "--env-name", help="Optional custom environment variable name to write the key to."),
):
    cfg = ConfigStore(); accounts = cfg.load_accounts()
    if group == "default":
        ref = env_name or f"TERMINALFORGE_{provider.value.upper()}_{name.upper().replace('-', '_')}"
    else:
        ref = env_name or f"TERMINALFORGE_{provider.value.upper()}_{group.upper().replace('-', '_')}_{name.upper().replace('-', '_')}"
    accounts = [a for a in accounts if not (a.provider == provider and a.name == name and a.group == group)]
    accounts.append(AccountProfile(provider=provider, name=name, group=group, label=label, model=model or None, secret_ref=ref))
    cfg.save_accounts(accounts)

    resolved_key = api_key or typer.prompt(f"API key for {group}/{provider.value}/{name}", hide_input=True)
    if resolved_key:
        SecretStore().set_local(ref, resolved_key)
        os.environ[ref] = resolved_key
        if env_name:
            os.environ[env_name] = resolved_key
        typer.echo(f"Saved API key for {group}/{provider.value}/{name} to {ref}")
        typer.echo(f"export {ref}='{resolved_key}'")
        if set_env:
            typer.echo(f"Environment is active for this session: {ref}={resolved_key[:4]}***")
    typer.echo(f"Added {group}/{provider.value}/{name}; secret env var: {ref}")

@account_app.command("list")
def account_list():
    for a in ConfigStore().load_accounts():
        typer.echo(f"{a.group:12} {a.provider.value:10} {a.name:18} {a.model or '-':24} {a.label}")

@module_app.command("list")
def module_list():
    for m in registry().all():
        typer.echo(f"{m.info.id:12} {m.info.name:20} {m.info.description}")

@module_app.command("run")
def module_run(module_id: str, mode: ExecutionMode | None = typer.Option(None, "--mode", "-m")):
    selected = mode or ConfigStore().load_mode()
    m = registry().get(module_id)
    if not m:
        raise typer.BadParameter(f"Unknown module: {module_id}")
    if selected == ExecutionMode.AI:
        typer.echo("AI mode requires `tf agent run`; module operations remain deterministic by default.")
    typer.echo(m.run_native())

@agent_app.command("frameworks")
def agent_frameworks():
    for name in AgentService().frameworks():
        typer.echo(name)

@agent_app.command("run")
def agent_run(prompt: str, framework: AgentFramework = typer.Option(AgentFramework.LANGCHAIN, "--framework", "-f"),
              account: str | None = typer.Option(None, "--account", "-a"), context: str = typer.Option("", "--context", "-c"),
              execute_tools: bool = typer.Option(False, "--execute-tools")):
    result = AgentService().run(AgentTask(objective=prompt, context=context, framework=framework, account=account, execute_tools=execute_tools))
    typer.echo(result.output)

def main():
    if len(sys.argv) == 1:
        from terminalforge.ui.app import TerminalForgeApp
        TerminalForgeApp(registry(), ConfigStore()).run()
    else:
        app()


if __name__ == "__main__":
    main()
