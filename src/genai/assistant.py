from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

from src.genai.settings import GEMINI_SETTINGS

from datetime import datetime


model = GeminiModel(GEMINI_SETTINGS.model_name, provider=GEMINI_SETTINGS.provider)

assistant_agent = Agent(
    model,
    system_prompt=(
        "Du bist ein hilfreicher und freundlicher Assistent. "
        "Deine Sprache ist 'deutsch', wenn nicht anders gefordert. "
        "Verwende die tools nur, wenn es sinnvoll ist. "
        "Für die Antwort dürfen Markdown-Formatierungen verwendet werden, ohne 'markdown' erwähnen zu müssen. "
    ),
    result_type=str,
    retries=2,
)


@assistant_agent.tool_plain
def current_time() -> str:
    """
    Gibt die aktuelle Uhrzeit zurück.
    """
    return datetime.now().strftime("%H:%M:%S %Y-%m-%d")
