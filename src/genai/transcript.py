from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

from src.genai.settings import GEMINI_SETTINGS


model = GeminiModel(GEMINI_SETTINGS.model_name, provider=GEMINI_SETTINGS.provider)

transcript_agent = Agent(
    model,
    system_prompt=(
        "Bitte transkribiere die Audiodatei präzise und exakt. "
        "Gib nur den reinen Transkriptionstext als Antwort zurück, ohne zusätzliche Informationen oder Erläuterungen. "
        "Die Antwort soll ausschließlich das Transkript enthalten."
    ),
    result_type=str,
    retries=2,
)
