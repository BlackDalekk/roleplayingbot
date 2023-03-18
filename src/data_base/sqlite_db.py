import sqlite3 as sq
import logging

from aiogram import types


class heroes_db:

    def __init__(self):
        self.base = sq.Connection
        self.cur = sq.Cursor

    def sql_start(self):
        self.base = sq.connect("heroes.db")
        self.cur = self.base.cursor()
        if self.base:
            logging.info(msg = "Data base connected!")
        self.base.execute(
            "CREATE TABLE IF NOT EXISTS heroes(userID INTEGER, name TEXT, biography TEXT)"
        )
        self.base.commit()

    async def sql_add_command(self, state, message: types.Message):
        async with state.proxy() as data:
            self.cur.execute(
                "INSERT INTO heroes VALUES (?, ?, ?)",
                (message.from_user.id, data["name"], data["biography"]),
            )
            self.base.commit()

    def is_in_the_database(self, message):
        is_in = self.cur.execute("SELECT * FROM heroes WHERE userID=?", (message.from_user.id,))
        return is_in.fetchone()  # None or not

    async def show_personal_data(self, message: types.Message):
        if self.is_in_the_database(message) is None:
            await message.answer("У вас нет персонажей")
        else:
            for ret in self.cur.execute("SELECT userID, name, biography FROM heroes").fetchall():
                # await message.answer(str(ret[0]) + ' ' + str(message.from_user.id))
                if int(ret[0]) == int(message.from_user.id):
                    await message.answer("Имя: " + ret[1] + "\nБиография: " + ret[-1])

    async def show_all_open_data(self, message: types.Message):
        for ret in self.cur.execute("SELECT userID, name, biography FROM heroes").fetchall():
            await message.answer("Имя: " + ret[1] + "\nБиография: " + ret[-1])

    async def delete_sql(self, message: types.Message):
        if self.is_in_the_database(message) is None:
            await message.answer("У вас нет персонажей")
        else:
            self.cur.execute("DELETE FROM heroes WHERE userID=?", (message.from_user.id,))
            await message.answer("Герой удален")
        self.base.commit()
