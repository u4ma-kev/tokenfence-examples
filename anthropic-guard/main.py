"""
TokenFence Anthropic Example

Protect Anthropic Claude API calls with per-workflow budgets.
Works the same way as OpenAI — wrap client.messages.create with fence.guard().
"""

from tokenfence import TokenFence, BudgetExceeded
import anthropic

client = anthropic.Anthropic()

# Guard Claude calls with a $3 budget
fence = TokenFence(
    budget=3.00,
    on_limit="downgrade",
    downgrade_map={
        "claude-sonnet-4-20250514": "claude-haiku-3-5-20241022",
    }
)

try:
    response = fence.guard(
        client.messages.create,
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Write a detailed analysis of..."}]
    )
    
    print(f"Response: {response.content[0].text[:100]}...")
    print(f"Cost: ${fence.tracker.total_cost:.4f}")
    print(f"Remaining: ${fence.tracker.remaining:.4f}")

except BudgetExceeded:
    print("Budget exceeded — agent stopped safely")
