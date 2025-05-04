"""
research_system.py

Defines the researcher (optimizer) and evaluator agents for the multi-agent system.
"""
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from models import ResearchAnswer, Feedback

load_dotenv()

# Define the MCP Servers
# tavily_mcp_server = MCPServerStdio(
#     command= "npx",
#     args=[
#         "-y",
#         "tavily-mcp@0.1.3"
#         ],
#     env= {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
# )

brave_search_mcp_server = MCPServerStdio(
    command= "npx",
    args=[
          "-y",
          "@modelcontextprotocol/server-brave-search"
        ],
    env= {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
)

# Researcher Agent (Agent A)
research_agent = Agent(
    model = "openai:gpt-4o",
    system_prompt=(
    """
    You are a research assistant. Answer the user's research question as thoroughly as possible. You may use the tavily MCP tool to gather additional information from the web.
    """
    ),
)

# research_agent = Agent[None, ResearchAnswer](
#     model = "openai:gpt-4o",
#     output_type=ResearchAnswer,
#     system_prompt=(
#     """
#     You are a research assistant. Answer the user's research question as thoroughly as possible. You may use the tavily MCP tool to gather additional information from the web.
#     """
#     ),
#     mcp_servers=[brave_search_mcp_server],
#     retries=2
# )


# Evaluator Agent (Agent B)
evaluator_agent = Agent(
    model = "openai:gpt-4o",
    output_type=Feedback,
    system_prompt=(
        """
        You are an evaluator. Given the proposed answer, decide if it fully addresses the research question.
        If the answer is incomplete or unclear, set 'accepted' to false and provide constructive feedback.
        """
    ),
)
