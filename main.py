"""
main.py

Entrypoint for running the multi-agent researcher system.
"""

import asyncio
from typing import Optional
from models import ResearchAnswer, Feedback # Although Feedback is not used directly here, it's good practice if modifying agent interactions
from research_system import research_agent, evaluator_agent
from pydantic_ai import format_as_xml

MAX_ITERATIONS = 5

# async def run_research_loop(question: str, max_iterations: int = MAX_ITERATIONS) -> Optional[ResearchAnswer]:
#     """
#     Runs the evaluator-optimizer loop for a research question.

#     Args:
#         question (str): The research question to answer.
#         max_iterations (int): Maximum number of iterations to attempt.

#     Returns:
#         Optional[ResearchAnswer]: The accepted answer, or None if not accepted within the limit.
#     """
#     async with research_agent.run_mcp_servers():
#     # Initial answer from Agent A
#         current_answer = await research_agent.run(question)
#         for i in range(max_iterations):
#             # Agent B evaluates the answer
#             feedback = await evaluator_agent.run(current_answer.output)
#             if feedback.output.accepted:
#                 print(f"Accepted on iteration {i+1}:")
#                 print(current_answer.output.text)
#                 return current_answer.output
#             # Prepare improved answer prompt for Agent A
#             improvement_prompt = (
#                 f"Improve this answer based on the following feedback:\n"
#                 f"Previous answer: {current_answer.output.text}\n"
#                 f"Feedback: {feedback.output.comments}"
#             )
#             current_answer = await research_agent.run(improvement_prompt)
#         print(f"Failed to converge within {max_iterations} iterations.")
#         return None

async def run_research_loop(question: str, max_iterations: int = MAX_ITERATIONS) -> Optional[ResearchAnswer]:
    """
    Runs the evaluator-optimizer loop for a research question.

    Args:
        question (str): The research question to answer.
        max_iterations (int): Maximum number of iterations to attempt.

    Returns:
        Optional[ResearchAnswer]: The accepted answer, or None if not accepted within the limit.
    """

# Initial answer from Agent A
    current_answer = await research_agent.run(question)
    for i in range(max_iterations):
        # Agent B evaluates the answer
        feedback_prompt = format_as_xml({'answer_to_evaluate': current_answer.output})
        feedback = await evaluator_agent.run(feedback_prompt)
        if feedback.output.accepted:
            print(f"Accepted on iteration {i+1}:")
            print(current_answer.output.text)
            return current_answer.output
        # Prepare improved answer prompt for Agent A
        improvement_prompt = (
            f"Improve this answer based on the following feedback:\n"
            f"Previous answer: {current_answer.output.text}\n"
            f"Feedback: {feedback.output.comments}"
        )
        current_answer = await research_agent.run(improvement_prompt)
    print(f"Failed to converge within {max_iterations} iterations.")
    return None
    

if __name__ == "__main__":
    # Example usage: replace with CLI or other input as needed
    user_question = "What are the main causes of climate change?"
    asyncio.run(run_research_loop(user_question))
