import os
import logging

from aiogram import types, Bot

from src.keyboards import main_menu_keyboard
from src.keyboards import make_row_keyboard
from src.keyboards import start_keyboard
from src.data_base.sqlite_db import heroes_db


class TelegramBot(Bot):

    def __init__(self, token: str) -> None:
        super().__init__(token=token)

        self.db = heroes_db()
        self.db.sql_start()

    async def command_start(self, message: types.Message):
        try:
            await self.send_message(
                message.from_user.id,
                "Привет, этот бот поможет тебе хранить твоих персонажей. Выбери действие",
                reply_markup=start_keyboard,
            )
            await message.delete()
        except:
            await message.answer(
                "Напишите боту личное сообщение: \nhttps://t.me/statisticsOfHero_bot"
            )

    @staticmethod
    async def help_func(message: types.Message):
        help_message = "Этот бот поможет тебе хранить твоих персонажей, экипировку и следить за своей историей"
        await message.answer(
            help_message,
            reply_markup=main_menu_keyboard,
        )
