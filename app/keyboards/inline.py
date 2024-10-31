# Import modules from aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Create inline key for add bot to the group
def add_bot() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Add to the group",
                          url="https://t.me/sumarizeebot?startgroup=true&admin=change_info+restrict_members+delete_messages+pin_messages+invite_users",
                          )]])

    return kb

# Create inline key for payment methods
def payment_methods() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Stars", callback_data='stars_payment')],
        [InlineKeyboardButton(text="Crypto", callback_data='crypto_payment')]
    ])
    
    return kb

# Create inline keyboard for crypto invoice
def crypto_invoice(invoice_url) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Pay", url=invoice_url)]
    ])

    return kb