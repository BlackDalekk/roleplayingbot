from email import message
import sqlite3 as sq
from telnetlib import NOP
from aiogram import types
#from create_bot import dp, bot

def sql_start():
    global base, cur
    base  = sq.connect('heroes.db')
    cur = base.cursor()
    if base:
        print('Data base connected!')
    base.execute('CREATE TABLE IF NOT EXISTS heroes(userID INTEGER, name TEXT, biography TEXT)')
    base.commit()

async def sql_add_command(state, message : types.Message):
    async with state.proxy() as data:
        cur.execute('INSERT INTO heroes VALUES (?, ?, ?)', (message.from_user.id, data['name'], data['biography']))
        base.commit()

def isInTheDatabase(message):
    isIn = cur.execute('SELECT * FROM heroes WHERE userID=?', (message.from_user.id, ))
    return isIn.fetchone() #None or not

async def showPersonalData(message : types.Message): 
    if isInTheDatabase(message) is None:
        await message.answer('У вас нет персонажей')
    else:
        for ret in cur.execute('SELECT userID, name, biography FROM heroes').fetchall():
            #await message.answer(str(ret[0]) + ' ' + str(message.from_user.id))
            if(int(ret[0]) == int(message.from_user.id)):
                await message.answer('Имя: ' + ret[1] + '\nБиография: ' + ret[-1])

async def delete_sql(message : types.Message):
    if isInTheDatabase(message) is None:
        await message.answer('У вас нет персонажей')
    else:
        cur.execute('DELETE FROM heroes WHERE userID=?', (message.from_user.id, ))
        await message.answer('Герой удален')