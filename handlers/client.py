from asyncore import dispatcher
from aiogram import types
from email import message
from create_bot import dp, bot



async def command_start(message : types.Message):
    await message.answer('Привет, этот бот поможет тебе хранить твоих персонажей')


async def add_new_hero(message : types.Message):
    await message.answer('Введите имя вашего нового героя')
    #code fsm


def register_handlers_client(dp : dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(add_new_hero, commands = ['add_new_hero' , 'добавить нового героя'])