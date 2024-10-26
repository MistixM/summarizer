from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.constants.wrap import (ADMIN, SUBSCRIPTION_BUTTON,
                                FAQ_BUTTON, SUPPORT_BUTTON,
                                INSTALLATION_BUTTON, POST_BUTTON, DEBUG_BUTTON)

def menu_keyboard(user_id):
    keyboard = [
        [KeyboardButton(text=INSTALLATION_BUTTON)],
        [KeyboardButton(text=SUBSCRIPTION_BUTTON), KeyboardButton(text=FAQ_BUTTON)],
        [KeyboardButton(text=SUPPORT_BUTTON)]
    ]

    if user_id == ADMIN:
        keyboard.append([KeyboardButton(text=POST_BUTTON), KeyboardButton(text=DEBUG_BUTTON)])

    kb = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    return kb