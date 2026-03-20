# TokenFence Quickstart

Get per-workflow budget protection in under 2 minutes.

## Install

```bash
# Python
pip install tokenfence

# Node.js / TypeScript
npm install tokenfence
```

## 1. Basic Budget Cap

### Python
```python
from tokenfence import guard
import openai

# Wrap your client — that's it
client = guard(openai.OpenAI(), budget="$0.50")

# Use normally — TokenFence tracks every call
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is 2+2?"}]
)
print(response.choices[0].message.content)

# Check your spend
print(f"Spent so far: ${client.tokenfence.spent:.4f}")
print(f"Remaining: ${client.tokenfence.remaining:.4f}")
```

### TypeScript
```typescript
import { guard } from "tokenfence";
import OpenAI from "openai";

const client = guard(new OpenAI(), { budget: "$0.50" });

const res = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "What is 2+2?" }],
});
console.log(res.choices[0].message.content);
console.log(`Spent: $${client.tokenfence.spent.toFixed(4)}`);
```

## 2. Auto-Downgrade + Kill Switch

```python
client = guard(
    openai.OpenAI(),
    budget="$1.00",
    fallback="gpt-4o-mini",  # Switch to this at 80% spend
    on_limit="stop",          # Return synthetic response at 100%
)

# Run a loop — TokenFence protects you automatically
for i in range(100):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Question {i}: explain quantum computing"}]
    )
    # At ~$0.80: silently switches to gpt-4o-mini
    # At $1.00: returns "[TokenFence] Budget exceeded" message
    print(f"Call {i}: ${client.tokenfence.spent:.4f} spent")
```

## 3. Multi-Agent Setup

```python
# Each agent gets its own budget — no blast radius
support = guard(openai.OpenAI(), budget="$0.10", on_limit="stop")
analyst = guard(openai.OpenAI(), budget="$1.00", fallback="gpt-4o-mini")
researcher = guard(openai.OpenAI(), budget="$5.00", fallback="gpt-4o-mini")

# If researcher goes haywire, it burns $5 max.
# Support and analyst keep working.
```

## 4. Anthropic

```python
import anthropic
from tokenfence import guard

client = guard(
    anthropic.Anthropic(),
    budget="$1.00",
    fallback="claude-3-haiku-20240307",
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarize this document..."}],
)
```

## Next Steps

- [API Reference](./api-reference.md) — full parameter docs
- [Examples](https://github.com/u4ma-kev/tokenfence-examples) — runnable example scripts
- [Blog](https://github.com/u4ma-kev/tokenfence-blog) — guides and deep dives
