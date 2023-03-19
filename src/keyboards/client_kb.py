from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str], one_time_keyboard: bool) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(
        keyboard=[row], resize_keyboard=True, one_time_keyboard=one_time_keyboard
    )


main_menu_keyboard = make_row_keyboard(
    [
        "/Добавить_нового_героя",
        "/Посмотреть_своих_героев",
        "/Удалить_героя",
        "/Посмотреть_всех_героев",
    ],
    True,
)

start_keyboard = make_row_keyboard(
    [
        "/Добавить_нового_героя",
        "/Посмотреть_всех_героев",
    ],
    True,
)
