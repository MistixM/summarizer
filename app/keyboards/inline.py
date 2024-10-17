from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def add_bot():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Add to the group", url="https://t.me/sumarizeebot?startgroup=true&admin=change_info+restrict_members+delete_messages+pin_messages+invite_users")]])

    return kb