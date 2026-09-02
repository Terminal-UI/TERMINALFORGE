from terminalforge.modules.base import ForgeModule, ModuleInfo

class MindForge(ForgeModule):
    info = ModuleInfo("ai", "MindForge", "Optional agentic AI workspace: LangChain, LangGraph and CrewAI", "AI")
    def run_native(self, **_) -> str:
        return "MindForge: AI is optional. Install `terminalforge[agentic]` and configure an account to enable it."
