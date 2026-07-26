import asyncio

from agents import Agent, AgentsException, ModelSettings, Runner, ToolTimeoutError

from .config import MODEL, MODEL_TEMPERATURE, OPENAI_API_KEY, logger
from .mcp import get_openai_mcp_server
from .prompts import SYSTEM_PROMPT


async def ask_agent(question: str):
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        async with get_openai_mcp_server() as mcp_server:
            agent = Agent(
                name="User Management Assistant",
                model=MODEL,
                instructions=SYSTEM_PROMPT,
                mcp_servers=[mcp_server],
                model_settings=ModelSettings(temperature=MODEL_TEMPERATURE),
            )
            result = await Runner.run(agent, question)
            return result.final_output

    except AgentsException as ex:
        logger.exception(str(ex))
        if ex.run_data:
            logger.exception("Last agent: %s", ex.run_data.last_agent.name)
            logger.exception("Raw responses: %s", ex.run_data.raw_responses)
            logger.exception("New items: %s", ex.run_data.new_items)

    except ToolTimeoutError as ex:
        logger.exception(ex.tool_name)
        logger.exception(ex.timeout_seconds)
        logger.exception(str(ex))

    except Exception as ex:
        logger.exception("Something went wrong!")
        logger.exception(type(ex).__name__)
        logger.exception(ex)


async def main() -> None:
    print("User Management OpenAI Agent")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        response = await ask_agent(question)
        print("\nAssistant:")
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
