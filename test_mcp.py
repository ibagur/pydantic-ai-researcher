"""
The script "test_mcp.py" is a demonstration of an interactive client that utilizes the Model Context Protocol (MCP) with Brave Search integration. The script performs the following steps:

1. **Environment Initialization:**  
   It begins by loading environment variables using the `dotenv` package, which is critical for retrieving sensitive information like the `BRAVE_API_KEY`.

2. **MCP Server Setup:**  
   An MCP server for Brave Search is initialized via `MCPServerStdio`. This server is launched using the command `npx -y @modelcontextprotocol/server-brave-search` with the API key passed via the environment.

3. **Agent Creation:**  
   The script creates an instance of an `Agent` with the GPT-4 model (`"openai:gpt-4o"`), integrating the Brave Search MCP server into its list of MCP servers. This configuration allows the Agent to leverage the functionalities provided by the MCP server.

4. **Asynchronous Interactive Loop:**  
   Inside the asynchronous `main()` function, the script enters an interactive loop:
   - It starts the MCP servers in an asynchronous context.
   - It prompts the user for input.
   - For each command (except when "exit" is typed), it sends the command along with conversation history to the Agent.
   - It prints the Agent's response and updates the conversation history, enabling context retention across interactions.

5. **Entry Point:**  
   The script concludes by running the asynchronous `main()` function using `asyncio.run(main())` if the script is executed as the main module.

Overall, the script showcases how to combine environment management, MCP server initialization, and asynchronous communication with an AI agent to provide an interactive user experience.
"""
# Load environment variables
from pydantic_ai import Agent
# Initialize MCPServerStdio for Brave Search integration
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

brave_search_mcp_server = MCPServerStdio(
# Create an Agent using OpenAI's GPT-4 and the configured MCP server
    command= "npx",
    args=[
          "-y",
          "@modelcontextprotocol/server-brave-search"
        ],
    env= {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
)

agent = Agent(model="openai:gpt-4o", mcp_servers=[brave_search_mcp_server])
async def main():
    """
    Executes the main asynchronous loop.
    
    This function initializes the MCP server, accepts user commands in a loop,
    processes them through the Agent, prints the Agent's response,
    and terminates when the user inputs 'exit'.
    """
    async with agent.run_mcp_servers():
        history = []
        while True:
            command = input("You: ")
            if command == "exit":
                break
            agent_response = await agent.run(command, message_history=history)
            print(f"Agent: {agent_response.output}")
            history += agent_response.new_messages()


if __name__ == "__main__":
    asyncio.run(main())
