
from src.settings import GEMINI_SETTINGS
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

MODEL = GeminiModel(
    model_name=GEMINI_SETTINGS.model_name, 
    provider=GEMINI_SETTINGS.provider
)

SYSTEM_PROMPT = (
    "Du bist ein hilfreicher Assistent, der auf Deutsch antwortet. "
    "Antworte immer wie eine australische 'Lisa'."
)

AGENT = Agent(
    model=MODEL,
    system_prompt=SYSTEM_PROMPT,
    result_type=str,
    retries=2
)