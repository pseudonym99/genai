from pathlib import Path

import chainlit as cl
from pydantic_ai import BinaryContent

from src.agent import AGENT


@cl.on_chat_start
async def on_chat_start():
    """
    Initialisiert eine neue Chat-Session. Erstellt eine leere Nachrichtenhistorie für den Benutzer.
    """
    cl.user_session.set("message_history", [])


@cl.on_message
async def call_agent(message: cl.Message):
    """
    Verarbeitet eingehende Benutzernachrichten und generiert Antworten.

    Args:
        message: Die Nachricht des Benutzers (kann Text und Anhänge enthalten)
    """
    # Nachrichtenhistorie aus der Session abrufen
    message_history = cl.user_session.get("message_history")

    # Antwort-Nachricht vorbereiten
    response_message = cl.Message(content="", author="Agent")

    # Nachrichteninhalt zusammenstellen (Text + optionale Anhänge)
    message_content = _build_message_content(message=message)

    # Agent aufrufen und Antwort streamen
    try:
        async with AGENT.run_stream(message_content, message_history=message_history) as agent_response:
            # Antwort Token für Token streamen
            async for text_chunk in agent_response.stream_text(delta=True):
                await response_message.stream_token(text_chunk)

        # Nachrichtenhistorie mit neuen Nachrichten aktualisieren
        updated_history = message_history + agent_response.all_messages()
        cl.user_session.set("message_history", updated_history)
    except Exception as error:
        response_message.content = f"Fehler bei der Verarbeitung: {error}"

    # Antwort an den Benutzer senden
    await response_message.send()


def _build_message_content(message: cl.Message) -> list:
    """
    Erstellt den vollständigen Nachrichteninhalt inklusive Anhängen.

    Args:
        message: Die Chainlit-Nachricht mit Text und optionalen Anhängen

    Returns:
        Liste mit Nachrichteninhalt (Text und binäre Inhalte)
    """
    content = [message.content]

    # Anhänge (z.B. Bilder) als BinaryContent hinzufügen
    for attachment in message.elements:
        binary_content = BinaryContent(data=Path(attachment.path).read_bytes(), media_type=attachment.mime)
        content.append(binary_content)

    return content
