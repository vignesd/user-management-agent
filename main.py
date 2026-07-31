"""OpenAI Agents CLI entry point.
Check User Managenment agent folder for full code
"""

import asyncio

from user_management_agent.cli_openai import main


if __name__ == "__main__":
    asyncio.run(main())
