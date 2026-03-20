# TokenFence Examples

Real-world examples of using TokenFence to protect your AI agent budgets.

## Examples

| Example | Description | Provider |
|---------|-------------|----------|
| [basic-budget](./basic-budget/) | Simple per-workflow budget with kill switch | OpenAI |
| [auto-downgrade](./auto-downgrade/) | Automatic model downgrade when budget runs low | OpenAI |
| [anthropic-guard](./anthropic-guard/) | Protect Anthropic Claude API calls | Anthropic |
| [multi-agent](./multi-agent/) | Budget tracking across a multi-agent workflow | OpenAI |

## Quick Start

```bash
pip install tokenfence
```

```python
from tokenfence import TokenFence

fence = TokenFence(budget=5.00)
response = fence.guard(
    client.chat.completions.create,
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(f"Cost so far: ${fence.tracker.total_cost:.4f}")
print(f"Budget remaining: ${fence.tracker.remaining:.4f}")
```

## License

MIT — use these examples however you like.
