from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def make_row_keyboard(items: list[str], one_time_keyboard : bool) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, one_time_keyboard=one_time_keyboard)
