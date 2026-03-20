# 🛡️ TokenFence Examples — Cost Circuit Breaker for AI Agents

> **Stop runaway AI costs in 2 lines of code.** Budget caps, automatic model downgrade, and kill switches for OpenAI, Anthropic, and Google Gemini.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

## The Problem

AI agents in production are a cost ticking bomb:

- **GPT-4o**: $10/1M output tokens
- **Claude Opus**: $75/1M output tokens
- **Average agent run**: 15-50 API calls
- **One bad loop**: 💸💸💸 surprise $200+ bill

A single runaway subagent loop can burn through your entire monthly budget in minutes. Rate limits don't help — they cap requests, not dollars.

## The Solution

```python
from tokenfence import guard
import openai

# That's it. $5 budget cap, auto-downgrade at 80%, kill at 100%.
client = guard(openai.OpenAI(), budget=5.00)

# Use normally — TokenFence tracks every token
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze this data..."}]
)
```

TokenFence wraps your existing OpenAI/Anthropic client with zero code changes:

- **Budget caps** — hard spending limits per workflow, per agent, per task
- **Auto model downgrade** — when spend hits 80%, automatically switch from GPT-4o → GPT-4o-mini
- **Kill switch** — hard stop when budget is exhausted, returns safe error instead of more spending
- **Cost tracking** — real-time spend visibility across all your agents

## Examples

| Example | What It Shows | Provider | Difficulty |
|---------|--------------|----------|------------|
| [basic-budget](./basic-budget/) | Simple per-workflow budget with kill switch | OpenAI | ⭐ Beginner |
| [auto-downgrade](./auto-downgrade/) | Automatic model downgrade when budget runs low | OpenAI | ⭐ Beginner |
| [anthropic-guard](./anthropic-guard/) | Protect Anthropic Claude API calls | Anthropic | ⭐ Beginner |
| [multi-agent](./multi-agent/) | Budget tracking across a multi-agent workflow | OpenAI | ⭐⭐ Intermediate |

## Documentation

- 📖 [Quickstart Guide](./docs/quickstart.md) — Get running in 5 minutes
- 📚 [API Reference](./docs/api-reference.md) — Full API docs with all parameters
- 💰 [Model Pricing Table](./docs/api-reference.md#supported-models--pricing) — 40+ models with current per-token costs

## Installation

### Python

```bash
pip install tokenfence

# With provider extras
pip install tokenfence[openai]        # OpenAI support
pip install tokenfence[anthropic]     # Anthropic support
pip install tokenfence[all]           # All providers
```

### Node.js / TypeScript

```bash
npm install tokenfence
```

```typescript
import { guard } from 'tokenfence';
import OpenAI from 'openai';

const client = guard(new OpenAI(), { budget: 5.00 });
```

## Why Not Just Use Rate Limits?

| Feature | Rate Limits | TokenFence |
|---------|------------|------------|
| Caps requests per minute | ✅ | — |
| Caps dollar spend | ❌ | ✅ |
| Per-workflow budgets | ❌ | ✅ |
| Auto model downgrade | ❌ | ✅ |
| Kill switch on overspend | ❌ | ✅ |
| Works across providers | ❌ | ✅ |
| Real-time cost tracking | ❌ | ✅ |

Rate limits protect the API provider. **TokenFence protects your wallet.**

## Supported Providers & Models

- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo, o1, o1-mini, o3-mini, GPT-5.4 mini/nano
- **Anthropic**: Claude Opus 4, Sonnet 4, Claude 3.7 Sonnet, Claude 3.5 Sonnet/Haiku, Claude 3 Opus/Sonnet/Haiku
- **Google**: Gemini 2.5 Pro/Flash, Gemini 2.0 Flash, Gemini 1.5 Pro/Flash
- **DeepSeek**: DeepSeek Chat, DeepSeek Reasoner

## Use Cases

- 🤖 **Multi-agent orchestration** — Give each agent its own budget envelope
- 🔄 **Automated pipelines** — Prevent cost blowups in CI/CD AI workflows
- 📊 **Cost allocation** — Track spend per feature, per user, per team
- 🛡️ **Production safety** — Hard kill switch prevents billing surprises
- 📉 **Smart degradation** — Automatically use cheaper models when budget is tight

## Links

- 🌐 [TokenFence Website](https://tokenfence.dev)
- 📦 Python SDK (coming soon on PyPI)
- 📦 Node.js SDK (coming soon on npm)
- 📝 [Blog: Why Your AI Agents Need a Cost Kill Switch](https://github.com/u4ma-kev/tokenfence-blog)

## License

MIT — use these examples however you like.
