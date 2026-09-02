from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel

class Provider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    KIMI = "kimi"
    GOOGLE = "google"

class ExecutionMode(StrEnum):
    NATIVE = "native"       # no AI dependency or credentials required
    AI = "ai"               # agentic execution
    HYBRID = "hybrid"       # deterministic tools + optional AI planning/review

class AccountProfile(BaseModel):
    provider: Provider
    name: str
    group: str = "default"
    label: str = ""
    model: str | None = None
    secret_ref: str | None = None
    enabled: bool = True

class ForgeModuleInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    ai_capable: bool = True
