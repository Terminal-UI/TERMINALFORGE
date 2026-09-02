from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ChatRequest:
    model: str
    prompt: str
    system: str | None = None

class AIProvider(Protocol):
    name: str
    def chat(self, request: ChatRequest, api_key: str) -> str: ...
