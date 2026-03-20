"""
TokenFence Multi-Agent Example

Track costs across an entire agent workflow where one agent
spawns sub-agents, each making their own API calls.

The shared TokenFence instance tracks cumulative spend.
"""

from tokenfence import TokenFence, BudgetExceeded

# One fence for the entire workflow — $10 total budget
workflow_fence = TokenFence(budget=10.00, on_limit="stop")


def research_agent(query: str):
    """Sub-agent that does research (multiple API calls)."""
    results = []
    for i in range(5):
        response = workflow_fence.guard(
            client.chat.completions.create,
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Research step {i}: {query}"}]
        )
        results.append(response)
    return results


def synthesis_agent(research_results: list):
    """Sub-agent that synthesizes research into a report."""
    response = workflow_fence.guard(
        client.chat.completions.create,
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Synthesize: {research_results}"}]
    )
    return response


def run_workflow(user_query: str):
    """Main orchestrator — spawns sub-agents, all sharing one budget."""
    try:
        # Research phase: 5 API calls
        research = research_agent(user_query)
        print(f"Research done. Spent: ${workflow_fence.tracker.total_cost:.4f}")

        # Synthesis phase: 1 API call
        report = synthesis_agent(research)
        print(f"Synthesis done. Spent: ${workflow_fence.tracker.total_cost:.4f}")

        return report

    except BudgetExceeded:
        print(f"🛑 Workflow budget exceeded!")
        print(f"Total spent: ${workflow_fence.tracker.total_cost:.4f}")
        print(f"The entire multi-agent workflow was capped at $10.00")
        return None


# Run it
run_workflow("What are the latest trends in AI agent frameworks?")
