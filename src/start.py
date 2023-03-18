import os
import logging

from aiogram.utils import executor

from telegram_bot import client
from telegram_bot.bot.bot import TelegramBot
from telegram_bot.dispatcher.telegram_dispatcher import TelegramDispatcher
from telegram_bot.client import ClientTelegramBot

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")


async def on_startup(_):
    logging.info(msg="Telegram bot is active")

try:
    tg_bot = TelegramBot(os.getenv('TOKEN'))
    logging.info(msg="Telegram bot created")

    dp = TelegramDispatcher(bot=tg_bot)
    logging.info(msg="Telegram dispatcher created")

    client = ClientTelegramBot(tg_bot)
    client.register_handlers(dp=dp)
    logging.info(msg="Registered client handlers")

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # on_start_up
except Exception as exc:
    logging.exception(msg="", exc_info=True)
    exit(1)





