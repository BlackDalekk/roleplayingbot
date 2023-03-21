from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher

from src.keyboards import main_menu_keyboard
from src.keyboards import make_row_keyboard


class CreatingNewHero(StatesGroup):
    name = State()
    biography = State()

    async def show_personal_heroes(self, message: types.Message):
        await self.db.show_personal_data(message)

    async def show_all_heroes(self, message: types.Message):
        await message.answer("Список всех cуществующих героев:")
        await self.db.show_all_open_data(message)

    async def start_creating_a_new_hero(self, message: types.Message):
        if self.db.is_in_the_database(message) is None:
            await CreatingNewHero.name.set()
            await message.answer(
                "Введи имя героя",
                reply_markup=make_row_keyboard(
                    ["/Отмена"], one_time_keyboard=bool(False)
                ),
            )
        else:
            await message.answer("Пока можно создать только одного персонажа")

    async def cancel_handler(self, message: types.Message, state):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer("ок", reply_markup=types.ReplyKeyboardRemove())

    async def set_a_name_for_the_hero(
            self, message: types.Message, state: CreatingNewHero
    ):
        async with state.proxy() as data:
            data["name"] = message.text
        await CreatingNewHero.next()
        await message.answer("Теперь Введи биографию")

    async def set_a_biography_for_the_hero(
            self, message: types.Message, state: CreatingNewHero
    ):
        async with state.proxy() as data:
            data["biography"] = message.text

        await message.answer(
            "Начинаем загружать на сервер", reply_markup=main_menu_keyboard
        )

        await self.db.add_hero(state, message)
        await message.answer("Данные сохранены")
        await state.finish()

    async def delete_the_hero(self, message: types.Message):
        await self.db.delete_sql(message)

    def register_handlers_client(self, dp: Dispatcher):
        dp.register_message_handler(self.command_start, commands=["start"])
        dp.register_message_handler(
            self.start_creating_a_new_hero,
            commands=["add_new_hero", "Добавить_нового_героя"],
            state=None,
        )
        dp.register_message_handler(
            self, self.cancel_handler, state="*", commands="Отмена"
        )
        dp.register_message_handler(
            self.cancel_handler, Text(equals="отмена", ignore_case=True), state="*"
        )
        dp.register_message_handler(
            self, self.show_personal_heroes, commands=["Посмотреть_своих_героев"]
        )
        dp.register_message_handler(
            self, self.show_all_heroes, commands=["Посмотреть_всех_героев"]
        )
        dp.register_message_handler(
            self, self.set_a_name_for_the_hero, state=CreatingNewHero.name
        )
        dp.register_message_handler(
            self, self.set_a_biography_for_the_hero, state=CreatingNewHero.biography
        )
        dp.register_message_handler(
            self, self.delete_the_hero, commands=["Удалить_героя"]
        )
        dp.register_message_handler(self, self.help_func, commands=["help"])

# добавить изменение данных - изменение биографии
# добавить админа - изменение любых данных, удадение любых данных, просмотр всех персонажей
# данные персонажа - фото, экипировка, класс, hp, мана
# открытая биография - закрытая биография
