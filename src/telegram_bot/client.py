from .dispatcher.telegram_dispatcher import TelegramDispatcher
from .bot.bot import TelegramBot


class ClientTelegramBot:

    def __init__(self, bot: TelegramBot) -> None:
        self.bot = bot

    def register_handlers(self, dp: TelegramDispatcher):
        dp.register_message_handler(self.bot.command_start, commands=['start'])
        dp.register_message_handler(self.bot.help_func, commands=['help'])

