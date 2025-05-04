import asyncio
from research_system import research_agent, evaluator_agent
from typing import Optional

MAX_ITERATIONS = 5

async def run_research_loop(max_iterations: int = MAX_ITERATIONS):
    """
    Runs the evaluator-optimizer loop for a research question.

    Args:
        question (str): The research question to answer.
        max_iterations (int): Maximum number of iterations to attempt.

    Returns:
        Optional[ResearchAnswer]: The accepted answer, or None if not accepted within the limit.
    """

# Initial answer from Agent A
    async with research_agent.run_mcp_servers():
        while True:
            command = input("You: ")
            if command == "exit":
                break
            current_answer = await research_agent.run(command)
            for i in range(max_iterations):
                # Agent B evaluates the answer
                feedback_prompt = current_answer.output
                feedback = await evaluator_agent.run(feedback_prompt)
                print(f"Feedback received: {feedback.output}")
                if feedback.output.accepted:
                    print(f"Accepted on iteration {i+1}:")
                    print(f"Answer: {current_answer.output}")
                    return
                # Prepare improved answer prompt for Agent A
                improvement_prompt = (
                    f"Improve this answer based on the following feedback:\n"
                    f"Previous answer: {current_answer.output}\n"
                    f"Feedback: {feedback.output.comments}"
                )
                current_answer = await research_agent.run(improvement_prompt)
            print(f"Failed to converge within {max_iterations} iterations.")
            return None


if __name__ == "__main__":
    # Example usage: replace with CLI or other input as needed
    #user_question = "What are the main causes of climate change?"
    asyncio.run(run_research_loop())
