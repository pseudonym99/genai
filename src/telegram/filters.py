from telegram import Update
from telegram.ext import filters

from src.telegram.settings import TELEGRAM_SETTINGS


class FilterAllowedUser(filters.UpdateFilter):
    name = "FilterAllowedUser"

    def filter(self, update: Update) -> bool:
        user_id = update.effective_user.id
        allowed = TELEGRAM_SETTINGS.check_user_id(user_id)
        print(allowed)
        return allowed


allowed_user_filter = FilterAllowedUser()