"""Test agent for `droneship run python --entrypoint agent.py`."""
import json
import os
import urllib.request

import langgraph  # proves the boot-time install of requirements.txt worked

print("agent.py running; langgraph imported from", os.path.dirname(langgraph.__file__))
names = sorted(k for k in os.environ if k.endswith(("_API_KEY", "_BASE_URL")))
print("model env vars:", names)

key = os.environ.get("ANTHROPIC_API_KEY")
base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
if not key:
    print("no ANTHROPIC_API_KEY: skipping the model call")
else:
    req = urllib.request.Request(
        base.rstrip("/") + "/v1/messages",
        data=json.dumps({
            "model": "claude-haiku-5-5",
            "max_tokens": 20,
            "messages": [{"role": "user", "content": "Reply with the single word pong."}],
        }).encode(),
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.load(r)
        print("model reply:", body["content"][0]["text"])
    except Exception as exc:  # report, don't crash: this is a probe
        print("model call failed:", exc)
