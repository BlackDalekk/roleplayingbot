from asyncore import dispatcher
from telnetlib import NOP
from aiogram import types
from email import message
from create_bot import dp, bot
from keyboards import kb_client, make_row_keyboard



async def command_start(message : types.Message):
    await message.answer('Привет, этот бот поможет тебе хранить твоих персонажей. Выбери действие',
    reply_markup=make_row_keyboard(['\Добавить нового героя',
                                    '\Посмотреть своих героев',
                                    '\Удалить героя']))


async def add_new_hero(message : types.Message):
    await message.answer('Давайте начнем', reply_markup=make_row_keyboard(["\привет", "\пока"]))
    #code fsm


async def show_personal_heroes(message : types.Message):
    #показывает твоих героев, подгружая из БД
    NOP

def register_handlers_client(dp : dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(add_new_hero, commands = ['add_new_hero' , 'добавить нового героя'])
    dp.register_message_handler(show_personal_heroes, commands = ['Посмотреть своих героев'])
