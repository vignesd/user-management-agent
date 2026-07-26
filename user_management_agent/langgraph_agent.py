import asyncio
from uuid import uuid4

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from .config import (
    MCP_SERVER_NAME,
    MCP_SERVER_URL,
    MODEL,
    MODEL_TEMPERATURE,
    OPENAI_API_KEY,
    logger,
)
from .mcp import get_langgraph_mcp_client
from .prompts import SYSTEM_PROMPT


def build_agent(tools):
    model = ChatOpenAI(model=MODEL, temperature=MODEL_TEMPERATURE)
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        name="user_management_langgraph_agent",
        checkpointer=InMemorySaver(),
    )


async def ask_agent(question: str, thread_id: str | None = None) -> str:
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        if not MCP_SERVER_URL:
            raise ValueError("MCP_SERVER_URL environment variable is not set.")

        client = get_langgraph_mcp_client()
        tools = await client.get_tools()
        agent = build_agent(tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]},
            config={"configurable": {"thread_id": thread_id or str(uuid4())}},
        )

        messages = result.get("messages", [])
        if not messages:
            return ""

        last_message = messages[-1]
        return getattr(last_message, "content", str(last_message))

    except Exception as ex:
        logger.exception("Something went wrong!")
        logger.exception(type(ex).__name__)
        logger.exception(ex)
        return "Sorry, something went wrong while running the agent."


async def main() -> None:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    if not MCP_SERVER_URL:
        raise ValueError("MCP_SERVER_URL environment variable is not set.")

    logger.info("Model: %s", MODEL)
    logger.info("Model Temperature: %s", MODEL_TEMPERATURE)
    logger.info("MCP Server URL: %s", MCP_SERVER_URL)
    logger.info("MCP Server Name: %s", MCP_SERVER_NAME)

    logger.info("=" * 50)
    logger.info(" User Management LangGraph Agent ")
    logger.info("=" * 50)
    logger.info("Type 'exit' to quit.\n")

    thread_id = str(uuid4())

    while True:
        question = input("\nYou: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        logger.info("Running agent...")
        response = await ask_agent(question, thread_id=thread_id)
        print("\nAssistant:")
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
