"""
Module: mcp_servers.py
Description: This script defines and configures the MCP servers used by the research system. It sets up three MCP servers:
- tavily_search_mcp_server: For specialized web-based research using the Tavily MCP.
- brave_search_mcp_server: For general web search tasks.
- arxiv_mcp_server: For querying academic papers via the arXiv MCP.
Each server is initialized using MCPServerStdio with appropriate command-line arguments and environmental variables.
"""
import os
from pydantic_ai.mcp import MCPServerStdio


# Define the MCP Servers
tavily_search_mcp_server = MCPServerStdio(
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

arxiv_mcp_server = MCPServerStdio(
    command= "npx",
    args=[
        "-y",
        "@smithery/cli@latest",
        "run",
        "arxiv-mcp-server",
        "--config",
        "{\"storagePath\":\"/Users/inigo/Documents/papers\"}"
        ]
)