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

class PersonalInfoOutput(BaseModel):
    contains_personal_info: bool
    reasoning: str


guardrail_agent = Agent(
    name="Homework check",
    instructions="Detect whether the user is asking for math homework help.",
    output_type=MathHomeworkOutput,
)

personal_info_agent = Agent(
    name="Personal info check",
    instructions="Detect whether the user is sharing personal information.",
    output_type=PersonalInfoOutput,
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

@input_guardrail
async def personal_info_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(personal_info_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_personal_info,
    )

agent = Agent(
    name="Customer support",
    instructions="Help customers with support questions.",
    input_guardrails=[math_guardrail, personal_info_guardrail],
)


async def main() -> None:
    try:
        question = "Can you solve 2x + 3 = 11 for me?"
        question = "Can you help to restart the laptop for me?"
        # question = "I want to share my personal information: My email is example@example.com"
        await Runner.run(agent, question)
        print("Request processed successfully.")
    except InputGuardrailTripwireTriggered:
        print("Guardrail blocked the request.")
        print("Reasoning:", agent.input_guardrails)


if __name__ == "__main__":
    asyncio.run(main())
