from __future__ import annotations
import httpx
from terminalforge.providers.base import ChatRequest

class OpenAICompatibleProvider:
    def __init__(self, name: str, base_url: str) -> None:
        self.name, self.base_url = name, base_url.rstrip("/")
    def chat(self, request: ChatRequest, api_key: str) -> str:
        messages = []
        if request.system: messages.append({"role":"system","content":request.system})
        messages.append({"role":"user","content":request.prompt})
        r = httpx.post(f"{self.base_url}/chat/completions", headers={"Authorization": f"Bearer {api_key}"}, json={"model":request.model,"messages":messages}, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
