# spectandi

[Spectandi](https://spectandi.com) is an AI agent observability and compliance platform. This SDK traces calls your agent makes to Anthropic's Claude models — capturing latency, token usage, cost, and status — and sends them to your Spectandi dashboard.

## Installation

```
pip install spectandi
```

## Quickstart

```python
import os
os.environ["SPECTANDI_API_KEY"] = "your-api-key-here"

from spectandi import tracked_chat

result = tracked_chat("Hello world", agent_name="my-first-agent")
print(result)
```

`tracked_chat()` wraps a single call to `client.messages.create()` (Anthropic) in an OpenTelemetry span, then exports that span to Spectandi over HTTPS. The return value is the model's text response, same as calling the Anthropic SDK directly.

### Getting an API key

Sign up at [spectandi.com](https://spectandi.com) and generate an API key from your dashboard.

### Configuration

Both of these can be set as environment variables (e.g. in a `.env` file, loaded automatically):

| Variable | Required | Description |
|---|---|---|
| `SPECTANDI_API_KEY` | Yes | Authenticates trace uploads to Spectandi. |
| `SPECTANDI_API_URL` | No | Defaults to the production Spectandi API. Override only for local/self-hosted testing. |

You'll also need `ANTHROPIC_API_KEY` set, since `tracked_chat()` calls the Anthropic API on your behalf.

### `tracked_chat()` parameters

| Parameter | Default | Description |
|---|---|---|
| `prompt` | — | The user message sent to the model. |
| `model` | `"claude-sonnet-4-6"` | Any Anthropic model name. |
| `max_tokens` | `500` | Passed through to the Anthropic API. |
| `agent_name` | `None` | Optional label shown in your Spectandi dashboard. |
| `session_id` | `None` | Optional label for grouping related calls. |
| `user_id` | `None` | Optional end-user label attached to the trace (not related to your Spectandi account). |

## What this does today

`tracked_chat()` traces a single Anthropic model call. It does not currently support other providers (e.g. OpenAI), multi-step or multi-agent tracing, or streaming responses.

---

This is an early release (0.x) — the interface may evolve as we learn from real usage. Feedback welcome at hello@spectandi.com.
