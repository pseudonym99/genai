from pathlib import Path
from typing import Literal, final

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_ai.providers.google_gla import GoogleGLAProvider


ROOT_DIRECTORY = Path(__file__).parent.parent.parent.absolute()


class GeminiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIRECTORY / '.env',
        env_file_encoding='utf-8',
        env_prefix='GEMINI_',
        case_sensitive=False,
        extra='ignore'
    )

    model_name: Literal["gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-2.5-pro-exp-03-25"] 
    api_key: SecretStr

    @property
    def provider(self):
        return GoogleGLAProvider(
            api_key=self.api_key.get_secret_value()
        )


GEMINI_SETTINGS: final = GeminiSettings()
