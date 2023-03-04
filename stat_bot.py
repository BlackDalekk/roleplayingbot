from distutils.cmd import Command
from aiogram.utils import executor
from create_bot import dp
from dataBase import sqlite_db
import os


async def on_startup(_):
    print("Бот активирован")
    sqlite_db.sql_start()


from handlers import client, admin, other

client.register_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
