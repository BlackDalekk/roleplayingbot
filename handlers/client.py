from asyncore import dispatcher
from distutils.cmd import Command
from imaplib import Commands
from multiprocessing.connection import answer_challenge
from telnetlib import NOP
from tokenize import String
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from email import message, message_from_binary_file
from create_bot import dp, bot
from keyboards import mainMenuKeyboard
from keyboards import make_row_keyboard

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from dataBase import sqlite_db


class CreatingNewHero(StatesGroup):
    name = State()
    biography = State()


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет, этот бот поможет тебе хранить твоих персонажей. Выбери действие',
                               reply_markup=make_row_keyboard(['/Добавить_нового_героя', '/Посмотреть_всех_героев'],
                                                              True))
        await message.delete()
    except:
        await message.answer('Напишите боту личное сообщение: \nhttps://t.me/statisticsOfHero_bot')


async def help_func(message: types.Message):
    await message.answer('/Посмотреть_своих_героев\n/Добавить_нового_героя\n/Удалить_героя',
                         reply_markup=mainMenuKeyboard)


async def show_personal_heroes(message: types.Message):
    await sqlite_db.show_personal_data(message)


async def show_all_heroes(message: types.Message):
    await message.answer('Список всех cуществующих героев:')
    await sqlite_db.show_all_open_data(message)


async def start_creating_a_new_hero(message: types.Message):
    if sqlite_db.is_in_the_database(message) is None:
        await CreatingNewHero.name.set()
        await message.answer('Введи имя героя',
                             reply_markup=make_row_keyboard(['/Отмена'], one_time_keyboard=bool(False)))
    else:
        await message.answer('Пока можно создать только одного персонажа')


async def cancel_handler(message: types.Message, state: CreatingNewHero):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('ок', reply_markup=types.ReplyKeyboardRemove())


async def set_a_name_for_the_hero(message: types.Message, state: CreatingNewHero):
    async with state.proxy() as data:
        data['name'] = message.text
    await CreatingNewHero.next()
    await message.answer('Теперь Введи биографию')


async def set_a_biography_for_the_hero(message: types.Message, state: CreatingNewHero):
    async with state.proxy() as data:
        data['biography'] = message.text

    await message.answer('Начинаем загружать на сервер', reply_markup=mainMenuKeyboard)

    await sqlite_db.sql_add_command(state, message)
    await message.answer('Данные сохранены')
    await state.finish()


async def delete_the_hero(message: types.Message):
    await sqlite_db.delete_sql(message)


def register_handlers_client(dp: dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(start_creating_a_new_hero, commands=['add_new_hero', 'Добавить_нового_героя'],
                                state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="Отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(show_personal_heroes, commands=['Посмотреть_своих_героев'])
    dp.register_message_handler(show_all_heroes, commands=['Посмотреть_всех_героев'])
    dp.register_message_handler(set_a_name_for_the_hero, state=CreatingNewHero.name)
    dp.register_message_handler(set_a_biography_for_the_hero, state=CreatingNewHero.biography)
    dp.register_message_handler(delete_the_hero, commands=['Удалить_героя'])
    dp.register_message_handler(help_func, commands=['help'])

# добавить изменение данных - изменение биографии
# добавить админа - изменение любых данных, удадение любых данных, просмотр всех персонажей
# данные персонажа - фото, экипировка, класс, hp, мана
# открытая биография - закрытая биография
