from pathlib import Path

import chainlit as cl

from src.genai.settings import GEMINI_SETTINGS
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel(GEMINI_SETTINGS.model_name, provider=GEMINI_SETTINGS.provider)
agent = Agent(
    model,
    system_prompt=(
        "Du bist ein hilfreicher Assistent, der auf Deutsch antwortet. "
    ),
    result_type=str,
    retries=2
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("message_history", [])


@cl.on_message
async def call_agent(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    msg = cl.Message(content="", author="Agent")
    
    content = [message.content]
    elements = message.elements
    
    for element in elements:
        content.append(
            BinaryContent(
                data=Path(element.path).read_bytes(),
                media_type=element.mime
            )
        )
        
    try:
        async with agent.run_stream(
            content,
            message_history=message_history
        ) as response:
            async for chunk in response.stream_text(delta=True):
                await msg.stream_token(chunk)
        
        message_history += response.all_messages()
        cl.user_session.set("message_history", message_history)
    except Exception as e:
        msg.content = f"Fehler: {e}"

    await msg.send()
