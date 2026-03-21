# Async Anthropic Example

Demonstrates using `async_guard()` with `anthropic.AsyncAnthropic`
for multi-step agent loops under a budget cap.

## Install

```bash
pip install tokenfence anthropic
```

## Run

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python main.py
```

## What It Shows

- Guarding async Anthropic calls in an agent loop
- 70% threshold for early downgrade to Haiku
- `on_limit='raise'` to catch budget exhaustion
- Multi-turn conversation tracking
