import asyncio

from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

# from .config import MODEL, MODEL_TEMPERATURE, OPENAI_API_KEY, logger


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Homework check",
    instructions="Detect whether the user is asking for math homework help.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(
    name="Customer support",
    instructions="Help customers with support questions.",
    input_guardrails=[math_guardrail],
)


async def main() -> None:
    try:
        await Runner.run(agent, "Can you solve 2x + 3 = 11 for me?")
    except InputGuardrailTripwireTriggered:
        print("Guardrail blocked the request.")


if __name__ == "__main__":
    asyncio.run(main())