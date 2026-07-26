import asyncio

from .openai_agent import ask_agent


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

