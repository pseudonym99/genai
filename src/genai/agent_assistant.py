from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel

from src.genai.settings import GEMINI_SETTINGS

from datetime import datetime


model = GeminiModel(
    GEMINI_SETTINGS.model_name, 
    provider=GEMINI_SETTINGS.provider
)

agent_assistant = Agent(
    model,
    system_prompt=(
        (
            "Du bist ein hilfreicher und freundlicher Assistent. "
            "Deine Sprache ist 'deutsch', wenn nicht anders gefordert. "
            "Verwende die tools nur, wenn es sinnvoll ist. "
            "Formatiere deine Antwort für eine Telegram-Nachricht. "
        )
    ),
    result_type=str,
    retries=2
)

@agent_assistant.tool_plain
def current_time() -> str:
    """
    Gibt die aktuelle Uhrzeit zurück.
    """
    return datetime.now().strftime("%H:%M:%S %Y-%m-%d")