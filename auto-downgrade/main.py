"""
TokenFence Auto-Downgrade Example

When your workflow hits 80% of its budget, TokenFence automatically
switches to a cheaper model. Your agent keeps running — just more efficiently.
"""

from tokenfence import TokenFence

# Create a fence that auto-downgrades when budget is 80% spent
fence = TokenFence(
    budget=5.00,
    on_limit="downgrade",
    downgrade_map={
        "gpt-4o": "gpt-4o-mini",           # $2.50/$10 → $0.15/$0.60 per 1M tokens
        "claude-sonnet-4-20250514": "claude-haiku-3-5-20241022",  # Similar savings
    }
)

# The guard() wrapper handles model switching transparently
response = fence.guard(
    client.chat.completions.create,
    model="gpt-4o",  # Starts with gpt-4o
    messages=[{"role": "user", "content": "Analyze this quarterly report..."}]
)

# Check what actually happened
print(f"Cost: ${fence.tracker.total_cost:.4f}")
print(f"Model used: {fence.last_model}")  # Might be gpt-4o-mini if budget was low
print(f"Budget remaining: ${fence.tracker.remaining:.4f}")
