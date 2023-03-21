from .dispatcher.telegram_dispatcher import TelegramDispatcher
from .bot.bot import TelegramBot
from .bot.stuctures import CreatingNewHero

class ClientTelegramBot:
    def __init__(self, bot: TelegramBot) -> None:
        self.bot = bot

    def register_handlers(self, dp: TelegramDispatcher):
        dp.register_message_handler(self.bot.command_start, commands=["start"])
        dp.register_message_handler(self.bot.help_func, commands=["help"])
        dp.register_message_handler(
            self.bot.start_creating_a_new_hero,
            commands=["Добавить_нового_героя", "добавить_нового_героя"],
        )
        dp.register_message_handler(
            self.bot.cancel_handler_creation_new_hero, commands=["Отмена", "отмена"]
        )
        dp.register_message_handler(self.bot.set_a_name_for_the_hero, state=CreatingNewHero.name)
        dp.register_message_handler(self.bot.set_hero_description, state=CreatingNewHero.description)
