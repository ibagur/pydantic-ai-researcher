"""
Module: research_system.py
Description: This script initializes the research system by loading environment variables via dotenv, configuring Pydantic AI models (including OpenAI variants), and setting up MCP servers for research and academic queries. It defines two agents: 
- research_agent: Answers research questions using specialized MCP servers (e.g., tavily search and arXiv search).
- evaluator_agent: Evaluates the answers provided by the research_agent, offering feedback for improvement.
"""
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from mcp_servers import tavily_search_mcp_server, brave_search_mcp_server, arxiv_mcp_server

load_dotenv()

# Direct OpenAI model
openai_model_simple = "gpt-4.1"
# Using OpenAIModel with OpenAIProvider
openai_model = OpenAIModel('gpt-4.1', provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY")))
# Using OllamaModel with custom OpenAIProvider
ollama_model = OpenAIModel(
    model_name='qwen3:30b', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

# Select the model to use for the agents
model = openai_model_simple

class Feedback(BaseModel):
    """
    Represents feedback from the evaluator agent.

    Attributes:
        accepted (bool): Indicates whether the answer is accepted.
        comments (str): Provides feedback or suggestions for improvement.
    """
    accepted: bool
    comments: str

# Researcher Agent (Agent A)
    # You are a research assistant. Answer the user's research question as thoroughly as possible. You may use the brave search MCP to gather general additional information and the tavily search MCP tool to gather more specialized information from the web.
research_agent = Agent(
    model = model,
    system_prompt=(
    """
    You are a research assistant. Answer the user's research question as thoroughly as possible. You may use the tavily search MCP tool to gather more specialized information from the web and the arxiv MCP tool for academic papers research.
    """
    ),
    mcp_servers=[tavily_search_mcp_server, arxiv_mcp_server],
    retries=2
)

# Evaluator Agent (Agent B)
evaluator_agent = Agent(
    model = model,
    output_type=Feedback,
    system_prompt=(
        """
        You are an evaluator. Given the proposed answer, decide if it fully addresses the research question.
        If the answer is incomplete or unclear, set 'accepted' to false and provide constructive feedback.
        """
    ),
)
