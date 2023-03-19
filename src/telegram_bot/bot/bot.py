from aiogram import types, Bot
from aiogram.dispatcher import FSMContext

from src.keyboards import main_menu_keyboard
from src.keyboards import make_row_keyboard
from src.keyboards import start_keyboard
from src.data_base.sqlite_db import HeroesDB
from . import stuctures as struct

from src.game_characters.hero.hero import Hero
from . import pars


class TelegramBot(Bot):

    def __init__(self, token: str) -> None:
        super().__init__(token=token)

        self.db = HeroesDB()
        self.db.sql_start()

    async def command_start(self, message: types.Message):
        try:
            await self.send_message(
                message.from_user.id,
                "Привет, этот бот поможет тебе хранить твоих персонажей. Выбери действие",
                reply_markup=start_keyboard,
            )
            await message.delete()
        except Exception:
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

    async def start_creating_a_new_hero(self, message: types.Message):
        #if self.db.is_in_the_database(message) is None:
        await struct.CreatingNewHero.name.set()
        await message.answer(
            "Введи имя героя",
            reply_markup=make_row_keyboard(
                ["/Отмена"], one_time_keyboard=bool(False)
            ),
        )
        #else:
            #await message.answer("Пока можно создать только одного персонажа")

    @staticmethod
    async def cancel_handler_creation_new_hero(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("Создание нового персонажа отменено", reply_markup=types.ReplyKeyboardRemove())

    @staticmethod
    async def set_a_name_for_the_hero(
            message: types.Message, state: FSMContext
    ):
        async with state.proxy() as data:
            data["name"] = message.text

        async with state.proxy() as data:
            Hero(pars.get_name_from_row_data(data), "").uploading_to_database(message.from_user.id)
        await state.finish()
