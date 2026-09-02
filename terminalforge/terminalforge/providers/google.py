from __future__ import annotations
import httpx
from terminalforge.providers.base import ChatRequest

class GoogleProvider:
    name = "google"
    def chat(self, request: ChatRequest, api_key: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{request.model}:generateContent"
        contents = [{"role":"user","parts":[{"text":request.prompt}]}]
        if request.system:
            contents.insert(0, {"role":"user","parts":[{"text":request.system}]})
        r = httpx.post(url, params={"key":api_key}, json={"contents":contents}, timeout=60)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
