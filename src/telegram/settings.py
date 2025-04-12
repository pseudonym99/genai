from pathlib import Path
from typing import final

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIRECTORY = Path(__file__).parent.parent.parent.absolute()


class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIRECTORY / '.env',
        env_file_encoding='utf-8',
        env_prefix='TELEGRAM_',
        case_sensitive=False,
        extra='ignore'
    )

    api_key: SecretStr
    chat_id: SecretStr


TELEGRAM_SETTIGNS: final = TelegramSettings()
