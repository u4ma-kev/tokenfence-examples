"""Async OpenAI with TokenFence budget guard.

Production AI agent pipelines run async. TokenFence's async_guard()
wraps AsyncOpenAI with the same budget caps, auto-downgrade, and kill switch.
"""

import asyncio
import openai
from tokenfence import async_guard


async def main():
    # Wrap an async OpenAI client with a $2 budget
    client = async_guard(
        openai.AsyncOpenAI(),
        budget="$2.00",
        fallback="gpt-4o-mini",
        on_limit="stop",
        threshold=0.8,
    )

    # Run multiple concurrent requests — all tracked against the same budget
    tasks = [
        client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"What is {i} + {i}?"}],
        )
        for i in range(5)
    ]

    responses = await asyncio.gather(*tasks)

    for i, resp in enumerate(responses):
        content = resp.choices[0].message.content
        print(f"Response {i}: {content[:60]}")

    # Check aggregate spend
    tracker = client.tokenfence
    print(f"\nTotal spent: ${tracker.spent:.4f}")
    print(f"Remaining:   ${tracker.remaining:.4f}")
    print(f"API calls:   {tracker.calls}")


if __name__ == "__main__":
    asyncio.run(main())
