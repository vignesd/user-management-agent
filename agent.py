import os
import logging

from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from agents.mcp import (
    MCPServerStreamableHttp,
    MCPServerStreamableHttpParams,
)

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4o-mini")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.2"))
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

SYSTEM_PROMPT = """
You are a User Management Assistant.

Rules:
- Always use MCP tools.
- Never make up user information.
- Choose the correct tool automatically.
- Explain your answer in simple English.
- Ask follow-up suggestions based on available tools.
"""


def get_mcp_server():
    return MCPServerStreamableHttp(
        name="User Management MCP",
        params=MCPServerStreamableHttpParams(
            url=MCP_SERVER_URL,
        ),
        cache_tools_list=True,
        max_retry_attempts=3,
        client_session_timeout_seconds=120,
    )


async def ask_agent(question: str):

    async with get_mcp_server() as mcp_server:

        agent = Agent(
            name="User Management Assistant",
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            mcp_servers=[mcp_server],
            model_settings=ModelSettings(temperature=MODEL_TEMPERATURE),
        )

        result = await Runner.run(agent, question)

        return result.final_output
