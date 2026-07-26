from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from langchain_mcp_adapters.client import MultiServerMCPClient

from .config import MCP_SERVER_NAME, MCP_SERVER_URL


def get_openai_mcp_server() -> MCPServerStreamableHttp:
    return MCPServerStreamableHttp(
        name=MCP_SERVER_NAME,
        params=MCPServerStreamableHttpParams(url=MCP_SERVER_URL),
        cache_tools_list=True,
        max_retry_attempts=3,
        client_session_timeout_seconds=120,
    )


def get_langgraph_mcp_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            MCP_SERVER_NAME: {
                "transport": "http",
                "url": MCP_SERVER_URL,
            }
        }
    )

