from distutils.cmd import Command
from email import message
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)



async def on_startup(_):
    print('Бот активирован')


@dp.message_handler(commands = ['start', 'help'])
async def command_start(message : types.Message):
    await message.answer('Привет, этот бот поможет тебе хранить твоих персонажей')


#@dp.message_handler()
#async def echo_send(message : types.Message):
    #await message.answer(message.text)
    #await message.reply(message.text)
    #await bot.send_message(message.from_user.id, message.text)

@dp.message_handler(commands = ['add_new_hero' , 'добавить нового героя'])
async def command_start(message : types.Message):
    await message.answer('Введите имя вашего нового героя')
    #code fsm






executor.start_polling(dp, skip_updates=True, on_startup=on_startup)