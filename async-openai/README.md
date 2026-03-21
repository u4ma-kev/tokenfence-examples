# Async OpenAI Example

Demonstrates using `async_guard()` with `openai.AsyncOpenAI` for concurrent
API calls under a shared budget.

## Install

```bash
pip install tokenfence[openai]
```

## Run

```bash
export OPENAI_API_KEY=sk-...
python main.py
```

## What It Shows

- Wrapping an async client with budget controls
- Running concurrent requests against a shared budget
- Auto-downgrade to cheaper model at 80% spend
- Kill switch when budget is exhausted
