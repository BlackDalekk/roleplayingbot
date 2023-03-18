from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.telegram_bot.bot.bot import TelegramBot


class TelegramDispatcher(Dispatcher):

    def __init__(self, bot: TelegramBot) -> None:
        storage = MemoryStorage()

        super().__init__(bot=bot, storage=storage)
