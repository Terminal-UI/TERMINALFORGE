from __future__ import annotations
import httpx
from terminalforge.providers.base import ChatRequest

class AnthropicProvider:
    name = "anthropic"
    def chat(self, request: ChatRequest, api_key: str) -> str:
        payload = {"model": request.model, "max_tokens": 2048, "messages":[{"role":"user","content":request.prompt}]}
        if request.system: payload["system"] = request.system
        r = httpx.post("https://api.anthropic.com/v1/messages", headers={"x-api-key":api_key,"anthropic-version":"2023-06-01","content-type":"application/json"}, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["content"][0]["text"]
