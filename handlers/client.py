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
from keyboards import make_row_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import os

class Creating_a_new_hero(StatesGroup):
    name = State()
    biography = State()

#C:\Users\a7987\OneDrive\Рабочий стол\tg_bot\data
async def save_data(data : list, username: str):
    os.chdir("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data\\" + username)
    with open(str(username+'.txt'), 'w') as f:
        f.write(str(data['name']))
        f.write('\n')
        f.write(str(data['biography']))
        f.write('\n')
        #os.mkdir(username)

async def command_start(message : types.Message):
    await message.answer('Привет, этот бот поможет тебе хранить твоих персонажей. Выбери действие',
    reply_markup=make_row_keyboard(['/Добавить_нового_героя',
                                    '/Посмотреть_своих_героев',
                                    '/Удалить_героя'], True))
    if not os.path.isdir("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data\\" + message.from_user.username):
        os.chdir("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data")
        os.mkdir(message.from_user.username)

async def help_func(message : types.Message):
    await message.answer('/Посмотреть_своих_героев\n/Добавить_нового_героя\n/Удалить_героя',
        reply_markup=make_row_keyboard(['/Добавить_нового_героя',
                                        '/Посмотреть_своих_героев',
                                        '/Удалить_героя'], True))

async def show_personal_heroes(message : types.Message):
    if os.path.isfile("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data\\" + message.from_user.username + "\\" + message.from_user.username + ".txt"):
        os.chdir("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data\\" + message.from_user.username)
        with open(str(message.from_user.username+'.txt'), 'r') as f:
            await message.answer('имя: ' + f.readline())
            await message.answer('биография: ' + f.readline())
    else:
        await message.answer('Сначала вам надо создать персонажа')

async def start_creating_a_new_hero(message : types.Message):
    await Creating_a_new_hero.name.set()
    await message.answer('Введи имя героя', reply_markup=make_row_keyboard(['/Отмена'], one_time_keyboard=bool(False)))

async def set_a_name_for_the_hero(message : types.Message, state : Creating_a_new_hero):
    async with state.proxy() as data:
        data['name'] = message.text #добавить проверку на \n и если нашли, то убрать
    await Creating_a_new_hero.next()
    await message.answer('Теперь Введи биографию')

async def set_a_biography_for_the_hero(message : types.Message, state : Creating_a_new_hero):
    async with state.proxy() as data:
        data['biography'] = message.text #добавить проверку на \n и если нашли, то убрать
        
    await message.answer('Начинаем загружать на сервер', reply_markup=make_row_keyboard(['/Добавить_нового_героя',
                                                         '/Посмотреть_своих_героев',
                                                         '/Удалить_героя'], True) )

    async with state.proxy() as data:
        await save_data(data, message.from_user.username)
    
    
    await message.answer('Данные сохранены')
    await state.finish()

async def cancel_handler(message : types.Message, state : Creating_a_new_hero):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('ок', reply_markup=types.ReplyKeyboardRemove())

async def delete_the_hero(message : types.Message):
    if os.path.isfile("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data\\" + message.from_user.username + "\\" + message.from_user.username + ".txt"):
        os.remove("C:\\Users\\a7987\\OneDrive\\Рабочий стол\\tg_bot\\data\\" + message.from_user.username + "\\" + message.from_user.username + ".txt")
        await message.answer('Герой удален')
    else:
        await message.answer('Сначала вам надо создать персонажа')


def register_handlers_client(dp : dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(cancel_handler, state="*", commands="Отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*") 
    dp.register_message_handler(show_personal_heroes, commands=['Посмотреть_своих_героев'])
    dp.register_message_handler(start_creating_a_new_hero, commands=['add_new_hero' , 'Добавить_нового_героя'], state = None)
    dp.register_message_handler(set_a_name_for_the_hero, state=Creating_a_new_hero.name)
    dp.register_message_handler(set_a_biography_for_the_hero, state=Creating_a_new_hero.biography)
    dp.register_message_handler(delete_the_hero, commands=['Удалить_героя'])
    dp.register_message_handler(help_func, commands=['help'])


    
