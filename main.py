import asyncio
import logging
import os

from agents import Agent, Runner
from agents.mcp import (
    MCPServerStreamableHttp,
    MCPServerStreamableHttpParams,
)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
# Stored API Key in system environment variable instead .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")


MODEL = os.getenv("MODEL", "gpt-5.5")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
MCP_SERVER_NAME = os.getenv("MCP_SERVER_NAME")
# -------------------------------------------------
# Configure Logging
# -------------------------------------------------
logger.info(
    f"Model - {MODEL}\nMCP Server URL - {MCP_SERVER_URL}\nMCP Server Name - {MCP_SERVER_NAME}"
)

SYSTEM_PROMPT = """
You are a User Management Assistant.

Rules:

- Always use MCP tools whenever possible.
- Never make up user information.
- Choose the correct tool automatically.
- If multiple tools exist, choose the best one.
- Explain your answer in simple English.
- If no suitable tool exists, say so politely.

"""

def get_mcp_server():
        logger.info("Connecting to MCP server...")
        mcp_server = MCPServerStreamableHttp(
            name="User Management MCP",
            params=MCPServerStreamableHttpParams(
                url=MCP_SERVER_URL,
            ),
            cache_tools_list=True,
            )
        return mcp_server


async def main():

    try:
        mcp_server=get_mcp_server()
        async with mcp_server:
            logger.info("Connected successfully.")
            logger.info("=" * 50)
            logger.info(" User Management AI Agent ")
            logger.info("=" * 50)
            logger.info("Type 'exit' to quit.\n")

            agent = Agent(
                name="User Assistant",
                model=MODEL,
                instructions=SYSTEM_PROMPT,
                mcp_servers=[mcp_server],
            )
            while True:
                question = input("\nYou: ")
                if question.lower() == "exit":
                    break
                logger.info("Running Agent...")
                result = await Runner.run(agent, question)
                print("\nAssistant:")
                print(result.final_output)

    except Exception as ex:
        logger.exception("Something went wrong!")
        logger.exception(ex)

async def show_available_tools():
    """
    Display all tools exposed by the MCP server.
    """
    try:
        logger.info("Fetching available tools...")
        mcp_server=get_mcp_server()
        async with mcp_server:
            tools = await mcp_server.list_tools()
        if not tools:
            logger.warning("No tools found.")
            return
        logger.info(f"Found {len(tools)} tool(s)\n")
        print("=" * 60)
        print("Available MCP Tools")
        print("=" * 60)
        for index, tool in enumerate(tools, start=1):
            print(f"\n{index}. {tool.name}")
            print(f"   Description : {tool.description}")
            # Print input schema if available
            if hasattr(tool, "inputSchema"):
                print(f"   Input Schema: {tool.inputSchema}")
        print("=" * 60)

    except Exception as ex:
        logger.exception(f"Unable to fetch tools: {ex}")

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(show_available_tools())
