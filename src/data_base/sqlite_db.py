import sqlite3 as sq
import logging

from aiogram import types


class HeroesDB:

    cur = sq.Cursor
    base = sq.Connection

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def sql_start(cls):
        cls.base = sq.connect("heroes.db")
        cls.cur = cls.base.cursor()
        if cls.base:
            logging.info(msg="Data base connected!")
        cls.base.execute(
            "CREATE TABLE IF NOT EXISTS heroes(userID INTEGER, name TEXT)"
        )
        cls.base.commit()

    @classmethod
    def add_hero(cls, user_id: int, data: dict):
        name = data["name"]
        cls.cur.execute(
                "INSERT INTO heroes VALUES (?, ?)",
                (user_id, name),
            )
        cls.base.commit()

    # @classmethod
    # def is_in_the_database(cls, message):
    #     is_in = cls.cur.execute("SELECT * FROM heroes WHERE userID=?", (message.from_user.id,))
    #     return is_in.fetchone()  # None or not
    #
    # @classmethod
    # async def show_personal_data(cls, message: types.Message):
    #     if cls.is_in_the_database(message) is None:
    #         await message.answer("У вас нет персонажей")
    #     else:
    #         for ret in cls.cur.execute("SELECT userID, name, biography FROM heroes").fetchall():
    #             # await message.answer(str(ret[0]) + ' ' + str(message.from_user.id))
    #             if int(ret[0]) == int(message.from_user.id):
    #                 await message.answer("Имя: " + ret[1] + "\nБиография: " + ret[-1])
    #
    # @classmethod
    # async def show_all_open_data(cls, message: types.Message):
    #     for ret in cls.cur.execute("SELECT userID, name, biography FROM heroes").fetchall():
    #         await message.answer("Имя: " + ret[1] + "\nБиография: " + ret[-1])
    #
    # @classmethod
    # async def delete_sql(cls, message: types.Message):
    #     if cls.is_in_the_database(message) is None:
    #         await message.answer("У вас нет персонажей")
    #     else:
    #         cls.cur.execute("DELETE FROM heroes WHERE userID=?", (message.from_user.id,))
    #         await message.answer("Герой удален")
    #     cls.base.commit()
