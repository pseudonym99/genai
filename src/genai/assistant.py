from textwrap import dedent

from pydantic_ai import Agent
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.models.gemini import GeminiModel

from src.genai.settings import GEMINI_SETTINGS

from datetime import datetime
import requests


model = GeminiModel(GEMINI_SETTINGS.model_name, provider=GEMINI_SETTINGS.provider)

assistant_agent = Agent(
    model,
    system_prompt=dedent(
        """# Rolle und Ziel:
        Du bist ein präziser KI-Assistent, der Telegram-Anfragen systematisch beantwortet.

        # Schritt-für-Schritt-Denkprozess (Schleife):
        1. Analysiere die Anfrage und ergänze fehlende Details. Nutze immer das Datum.
        2. Bestimme die nötigen Informationen. Wenn Informationen oder URLs fehlen, nutze DuckDuckgo, 
            um relevante Websites zu finden. Das darfst du immer tun, ohne nachzufragen.
        4. Verwende get_text_from_website, um detaillierte Inhalte zu den URLs abzurufen.
        5. Prüfe kritisch, ob das Ergebnis vollständig und zufriedenstellend ist.
        6. Wiederhole Schritt 2 bis 5, bis ein zufriedenstellendes Ergebnis erzielt ist. 
            Dabei dürfen die Tools auch mehrfach verwendet werden.
        7. Antworte erst, wenn alle Details geliefert wurden. Die Antwort muss immer das Ergebnis enthalten.

        # Formatierung:
        Formatiere deine Antworten übersichtlich in Telegram Markdown V2.
        """
    ),
    result_type=str,
    retries=8,
    tools=[duckduckgo_search_tool()],
    result_retries=3
)

@assistant_agent.system_prompt
def get_current_date() -> str:
    """Use this tool to get the current date and time."""
    return f"Das aktuelle Datum ist: {datetime.now().isoformat()}"


@assistant_agent.tool_plain
def get_details_from_website_url(website_url: str) -> str:
    """Use this tool everytime to get detailed content from a website URL."""
    response = requests.get(website_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

