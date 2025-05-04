import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic import BaseModel

load_dotenv()

# Define the MCP Servers
tavily_mcp_server = MCPServerStdio(
    command= "npx",
    args=[
        "-y",
        "tavily-mcp@0.1.3"
        ],
    env= {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
)

brave_search_mcp_server = MCPServerStdio(
    command= "npx",
    args=[
          "-y",
          "@modelcontextprotocol/server-brave-search"
        ],
    env= {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
)

class Feedback(BaseModel):
    """
    Represents feedback from the evaluator agent.

    Attributes:
        accepted (bool): Whether the answer is accepted.
        comments (str): Feedback or suggestions for improvement.
    """
    accepted: bool
    comments: str

# Researcher Agent (Agent A)
research_agent = Agent(
    model = "openai:gpt-4o",
    system_prompt=(
    """
    You are a research assistant. Answer the user's research question as thoroughly as possible. You may use the brave search MCP tool to gather additional information from the web.
    """
    ),
    mcp_servers=[brave_search_mcp_server],
    retries=2
)

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
