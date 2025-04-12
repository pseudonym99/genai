from pathlib import Path
from typing import final

from pydantic import Field, SecretStr
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
    allowed_user_ids: list[SecretStr] = Field(default_factory=list)
    
    def check_user_id(self, user_id: int) -> bool:
        """
        Check if the provided user ID is in the allowed list.
        """
        return str(user_id) in [str(user_id.get_secret_value()) for user_id in self.allowed_user_ids]


TELEGRAM_SETTINGS: final = TelegramSettings()
