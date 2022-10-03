from asyncore import dispatcher
from distutils.cmd import Command
from imaplib import Commands
from multiprocessing.connection import answer_challenge
from telnetlib import NOP
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from email import message
from create_bot import dp, bot
from keyboards import make_row_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

class Creating_a_new_hero(StatesGroup):
    name = State()
    biography = State()



async def command_start(message : types.Message):
    await message.answer('Привет, этот бот поможет тебе хранить твоих персонажей. Выбери действие',
    reply_markup=make_row_keyboard(['/Добавить_нового_героя',
                                    '/Посмотреть_своих_героев',
                                    '/Удалить_героя'], True))

async def show_personal_heroes(message : types.Message):
    #показывает твоих героев, подгружая из БД
    NOP

async def start_creating_a_new_hero(message : types.Message):
    await Creating_a_new_hero.name.set()
    await message.answer('Введи имя героя', reply_markup=make_row_keyboard(['/Отмена'], one_time_keyboard=bool(False)))

async def set_a_name_for_the_hero(message : types.Message, state : Creating_a_new_hero):
    async with state.proxy() as data:
        data['name'] = message.text
    await Creating_a_new_hero.next()
    await message.answer('Теперь Введи биографию')

async def set_a_biography_for_the_hero(message : types.Message, state : Creating_a_new_hero):
    async with state.proxy() as data:
        data['biography'] = message.text
    async with state.proxy() as data:
        await message.answer(str(data), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

async def cancel_handler(message : types.Message, state : Creating_a_new_hero):
    await message.answer('123')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('ок', reply_markup=types.ReplyKeyboardRemove())

def register_handlers_client(dp : dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler, state="*", commands="Отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*") 
    dp.register_message_handler(show_personal_heroes, commands=['Посмотреть_своих_героев'])
    dp.register_message_handler(start_creating_a_new_hero, commands=['add_new_hero' , 'Добавить_нового_героя'], state = None)
    dp.register_message_handler(set_a_name_for_the_hero, state=Creating_a_new_hero.name)
    dp.register_message_handler(set_a_biography_for_the_hero, state=Creating_a_new_hero.biography)


    
