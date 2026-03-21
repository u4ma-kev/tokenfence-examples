"""Async Anthropic with TokenFence budget guard.

Guards an AsyncAnthropic client with per-workflow budget caps.
Perfect for agentic loops where Claude calls can snowball.
"""

import asyncio
import anthropic
from tokenfence import async_guard


async def agent_loop():
    # $1 budget for this workflow — raises BudgetExceeded when exhausted
    client = async_guard(
        anthropic.AsyncAnthropic(),
        budget="$1.00",
        fallback="claude-3-haiku-20240307",
        on_limit="raise",
        threshold=0.7,  # Start downgrading at 70%
    )

    messages = []
    prompts = [
        "Write a Python function to parse CSV files",
        "Now add error handling for malformed rows",
        "Add type hints and a docstring",
    ]

    for prompt in prompts:
        messages.append({"role": "user", "content": prompt})

        try:
            response = await client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=messages,
            )
            reply = response.content[0].text
            messages.append({"role": "assistant", "content": reply})
            print(f"✅ Step done — spent ${client.tokenfence.spent:.4f}")
        except Exception as e:
            print(f"⛔ Budget hit: {e}")
            break

    print(f"\nFinal: ${client.tokenfence.spent:.4f} / ${client.tokenfence.budget:.2f}")


if __name__ == "__main__":
    asyncio.run(agent_loop())
