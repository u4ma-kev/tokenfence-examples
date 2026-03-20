# TokenFence API Reference

## `guard(client, *, budget, fallback=None, on_limit="stop", threshold=0.8)`

Wraps an OpenAI or Anthropic client with cost tracking and budget enforcement. Returns a drop-in replacement for the original client.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `client` | `openai.OpenAI` or `anthropic.Anthropic` | *required* | The AI client to wrap |
| `budget` | `str \| float \| int` | *required* | Max spend in USD. Accepts `"$0.50"` or `0.50` |
| `fallback` | `str \| None` | `None` | Model to auto-downgrade to when threshold is reached |
| `on_limit` | `"stop" \| "warn" \| "raise"` | `"stop"` | Behaviour when budget is exhausted |
| `threshold` | `float` | `0.8` | Fraction (0.0–1.0) of budget at which to trigger downgrade |

### Returns

A `GuardedClient` that proxies all calls to the original client. Use it exactly as you would the original.

### Raises

- `TokenFenceError` — invalid budget, threshold, or on_limit value
- `BudgetExceeded` — (only when `on_limit="raise"`) budget has been exhausted

---

## `on_limit` Modes

### `"stop"` (default)
Returns a synthetic response with zero tokens used. Your code keeps running — the response content will be `"[TokenFence] Budget of $X.XX exceeded (spent $X.XXXX). Request blocked."`.

### `"warn"`
Logs a warning via Python's `logging` module (logger name: `"tokenfence"`), then allows the API call through. Use when you want visibility without hard stops.

### `"raise"`
Raises `BudgetExceeded` exception. Catch it to implement custom logic:

```python
from tokenfence import guard, BudgetExceeded

client = guard(openai.OpenAI(), budget="$0.50", on_limit="raise")

try:
    response = client.chat.completions.create(model="gpt-4o", messages=[...])
except BudgetExceeded as e:
    print(f"Spent ${e.spent:.4f} of ${e.budget:.2f} budget")
    # Switch to manual fallback, cache, or abort
```

---

## `client.tokenfence` — CostTracker

Every guarded client exposes a `.tokenfence` attribute with real-time spend data.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `spent` | `float` | Total USD spent so far |
| `budget` | `float` | Total budget in USD |
| `remaining` | `float` | Budget minus spent (`budget - spent`) |
| `usage_ratio` | `float` | Fraction of budget used (`spent / budget`) |
| `should_downgrade` | `bool` | `True` when `usage_ratio >= threshold` |
| `budget_exceeded` | `bool` | `True` when `spent >= budget` |
| `call_count` | `int` | Number of API calls tracked |

### Methods

| Method | Description |
|--------|-------------|
| `record(cost: float)` | Manually record a cost (called automatically by guard) |
| `reset()` | Reset spent to 0 and call_count to 0 |

### Example

```python
client = guard(openai.OpenAI(), budget="$1.00")

# After some API calls...
print(f"Spent: ${client.tokenfence.spent:.4f}")
print(f"Remaining: ${client.tokenfence.remaining:.4f}")
print(f"Calls: {client.tokenfence.call_count}")
print(f"Usage: {client.tokenfence.usage_ratio:.1%}")
```

---

## Supported Models & Pricing

TokenFence includes built-in pricing for 40+ models:

### OpenAI
| Model | Input ($/1M) | Output ($/1M) |
|-------|-------------|---------------|
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-4-turbo | $10.00 | $30.00 |
| gpt-4 | $30.00 | $60.00 |
| gpt-3.5-turbo | $0.50 | $1.50 |
| o1 | $15.00 | $60.00 |
| o1-mini | $3.00 | $12.00 |
| o3-mini | $1.10 | $4.40 |
| gpt-5.4 | $5.00 | $15.00 |
| gpt-5.4-mini | $0.30 | $1.20 |
| gpt-5.4-nano | $0.10 | $0.40 |

### Anthropic
| Model | Input ($/1M) | Output ($/1M) |
|-------|-------------|---------------|
| claude-opus-4-20250514 | $15.00 | $75.00 |
| claude-sonnet-4-20250514 | $3.00 | $15.00 |
| claude-3-7-sonnet | $3.00 | $15.00 |
| claude-3-5-sonnet-20241022 | $3.00 | $15.00 |
| claude-3-5-haiku-20241022 | $0.80 | $4.00 |
| claude-3-haiku-20240307 | $0.25 | $1.25 |

### Google
| Model | Input ($/1M) | Output ($/1M) |
|-------|-------------|---------------|
| gemini-2.5-pro | $1.25 | $10.00 |
| gemini-2.5-flash | $0.15 | $0.60 |
| gemini-2.0-flash | $0.10 | $0.40 |
| gemini-1.5-pro | $1.25 | $5.00 |

### DeepSeek
| Model | Input ($/1M) | Output ($/1M) |
|-------|-------------|---------------|
| deepseek-chat | $0.14 | $0.28 |
| deepseek-reasoner | $0.55 | $2.19 |

---

## Exceptions

### `TokenFenceError`
Base exception for all TokenFence errors.

### `BudgetExceeded(TokenFenceError)`
Raised when `on_limit="raise"` and the budget is exhausted.

**Attributes:**
- `budget: float` — the total budget
- `spent: float` — the amount spent

---

## Thread Safety

`CostTracker` uses `threading.Lock` internally. Multiple threads sharing the same guarded client will correctly accumulate costs without race conditions.

---

## Framework Compatibility

TokenFence works with any framework that uses the standard OpenAI or Anthropic Python/Node.js SDKs:

- ✅ LangChain / LangGraph
- ✅ CrewAI
- ✅ AutoGen
- ✅ Custom agent loops
- ✅ FastAPI / Flask backends
- ✅ Jupyter notebooks

No special adapters needed — just wrap the client before passing it to your framework.
