"""
TokenFence Basic Budget Example

Demonstrates per-workflow budget enforcement with a hard kill switch.
When the budget is exceeded, BudgetExceeded is raised.
"""

from tokenfence import TokenFence, BudgetExceeded

# Create a fence with a $2.00 budget
fence = TokenFence(budget=2.00, on_limit="stop")

# Simulate guarding an OpenAI call
# In production, pass your actual client.chat.completions.create
try:
    # Each call is tracked against the $2 budget
    for i in range(100):
        response = fence.guard(
            your_openai_client.chat.completions.create,
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Task {i}: summarize this document..."}]
        )
        print(f"Call {i}: ${fence.tracker.total_cost:.4f} spent, ${fence.tracker.remaining:.4f} remaining")

except BudgetExceeded as e:
    print(f"\n🛑 Budget exceeded after {i} calls!")
    print(f"Total spent: ${fence.tracker.total_cost:.4f}")
    print(f"Budget was: $2.00")
    print("Agent stopped safely — no runaway costs.")
