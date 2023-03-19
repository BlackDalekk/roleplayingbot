from aiogram.dispatcher.filters.state import State, StatesGroup


class CreatingNewHero(StatesGroup):
    name = State()
    description = State()
