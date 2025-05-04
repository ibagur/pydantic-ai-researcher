from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

brave_search_mcp_server = MCPServerStdio(
    command= "npx",
    args=[
          "-y",
          "@modelcontextprotocol/server-brave-search"
        ],
    env= {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
)

agent = Agent(model="openai:gpt-4o", mcp_servers=[brave_search_mcp_server])
async def main():
    async with agent.run_mcp_servers():
        while True:
            command = input("You: ")
            if command == "exit":
                break
            agent_response = await agent.run(command)
            print(f"Agent: {agent_response.output}")


if __name__ == "__main__":
    asyncio.run(main())
