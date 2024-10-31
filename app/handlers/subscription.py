import datetime
import aiohttp
import uuid
import hashlib
import json
import base64
import asyncio

# Import aiogram dependencies
from aiogram import Bot, F, types, Router
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.exceptions import TelegramForbiddenError

# Import app dependencies (wraps, keyboards, databases)
from app.constants.wrap import (SUBSCRIPTION_DESCRIPTION, SUBSCRIPTION_SUCCESS, 
                                SUBSCRIOTION_HAVE, SUBSCRIPTION_PRICE,
                                SUBSCRIPTION_BUTTON, SUBSCRIPTION_PRICE_DOLLAR)

from app.keyboards.inline import payment_methods, crypto_invoice

from app.database.db import (update_user_data, check_user_data, 
                             get_all_chats, check_chat_data, 
                             update_chat_data, remove_chat)

import configparser

# Create separate router
sub_router = Router()

config = configparser.ConfigParser()
config.read('./app/constants/config.ini')

print(config['Bot']['TOKEN'])

# Handle subscription command
@sub_router.message(Command(commands=['subscription']))
@sub_router.message(lambda msg: msg.text == SUBSCRIPTION_BUTTON)
async def subscription(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    # Again filter current chat
    if not "-" in str(chat_id):
        await bot.send_message(chat_id, 
                                f"{SUBSCRIPTION_DESCRIPTION}",
                                parse_mode='HTML',
                                reply_markup=payment_methods(),
                                disable_web_page_preview=True)
        
    # If user requested subscription not in the DM
    else:
        await bot.send_message(chat_id,
                            f"⭐ Make your chat more free with subscription! To continue please request subscription in the bot")


# Router callback handler        
@sub_router.callback_query(lambda d: d.data)
async def handle_payment_callbacks(callback: CallbackQuery):
    # Split callback and define payment method
    method = callback.data.split('_')

    # Write other important information
    chat_id = callback.message.chat.id
    user_data = check_user_data(chat_id)

    # If user is already subscribed, just notify about it
    if user_data['is_vip']:
        expiration_date_iso = user_data['expiration_date']
        expiration_date = datetime.datetime.fromisoformat(expiration_date_iso)

        await callback.bot.send_message(callback.message.chat.id, 
                                        text=f"<b>{SUBSCRIOTION_HAVE}{expiration_date.strftime('%d.%m.%y')}</b>",
                                        parse_mode='HTML')
        return
    
    # Handle chosen payment method (either stars or crypto)
    if method[0] == "stars":
        # Generate invoice for the stars
        await callback.bot.send_invoice(chat_id,
                        title="Premium Subscription",
                        description="Monthly premium subscription that includes 1 minute cooldown and message memorize",
                        payload="private",
                        currency="XTR",
                        prices=[LabeledPrice(label='XTR', amount=SUBSCRIPTION_PRICE)],
                        )
        
    elif method[0] == "crypto":
        # Create invoice
        invoice_data = await make_crypto_request(
            url="https://api.cryptomus.com/v1/payment",
            invoice_data={
                "amount": str(round(SUBSCRIPTION_PRICE_DOLLAR)),
                "currency": "USD",
                "order_id": str(uuid.uuid4())
            },
        )

        # Create invoice checker task
        asyncio.create_task(
            check_invoice_status(invoice_data['result']['uuid'],
                                 message=callback.message)
        )

        # Send message to the user with the invoice ID and URL
        await callback.bot.send_message(chat_id,
                                        f"💸 Bot uses Cryptomus as a crypto payment system. Please use the following link to continue payment.\n\nYour invoice ID: <code>{invoice_data['result']['uuid']}</code>",
                                        parse_mode='HTML',
                                        reply_markup=crypto_invoice(invoice_data['result']['url']))

# Pre-checkout. Here, if necessary, you can check if product exist (i think, not in project case)
@sub_router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)

# Successful payment callback handler
@sub_router.message(F.successful_payment)
async def successful_payment(msg: types.Message):
    await send_successful_message(msg)

    # Refund only with test purpose. On production we don't want to refund stars
    # await msg.bot.refund_star_payment(chat_id,
    #                                   msg.successful_payment.telegram_payment_charge_id)
    
# A function that will create crypto request to cryptomus system
async def make_crypto_request(url: str, invoice_data: dict):
    encoded_data = base64.b64encode(
        json.dumps(invoice_data).encode('utf-8')
    ).decode('utf-8')
    signature = hashlib.md5(f"{encoded_data}{config['Bot']['CRYPTOMUS_TOKEN']}".encode('utf-8')).hexdigest()

    async with aiohttp.ClientSession(headers={
        "merchant": config['Bot']['CRYPTOMUS_MERCHANT'],
        "sign": signature,
    }) as session:
        async with session.post(url=url, json=invoice_data) as response:
            if not response.ok:
                return response.reason
            
            return await response.json()

# A function that will check invoice status in while loop
async def check_invoice_status(id: str, message):
    while True:
        try:
            invoice_data = await make_crypto_request(
                url="https://api.cryptomus.com/v1/payment/info",
                invoice_data={"uuid": id}
            )
        except Exception as e:
            print(f"An error occured while invoice check: {e}")
            break

        if invoice_data['result']['payment_status'] in ("paid", "paid_over"):
            await send_successful_message(message) 
            break

        await asyncio.sleep(10)

# Will send successful message to the specified chat
async def send_successful_message(msg) -> None:
    chat_id = msg.chat.id

    # Generate expiration date (month)
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=31)

    # Reply to user about successul payment with expiration info
    await msg.reply(f"<b>{SUBSCRIPTION_SUCCESS}{expiration_date.strftime('%d.%m.%y')}</b>", parse_mode='HTML')
    
    # Write all necessary values into the database
    update_user_data(chat_id, "is_vip", True)
    update_user_data(chat_id, "expiration_date", expiration_date.isoformat())
    update_user_data(chat_id, "reminded", False)

    # Get all chats from the database
    chats = get_all_chats()

    # User info
    user = await msg.bot.get_chat(chat_id)

    # Check each chat and send notification about owner's VIP
    # And set vip status for each group if it's equals to owner's ID
    for chat in chats:

        try:
            chat_info = check_chat_data(chat)
            owner = chat_info.get("b_owner")
            
            if owner and owner == chat_id:
                update_chat_data(chat, "vip", True)
                await msg.bot.send_message(chat, f"🤩 Congratulations to @{user.username}! Now the chat has a VIP status", parse_mode='markdown')
            else:
                continue
        
        # Important. This block of code will check type of error message.
        # Because somtimes bot can be blocked or have another issues.
        # For checking bot status in the chat, I inserted approximate error message in conditions
        except TelegramForbiddenError as e:
            if "bot was kicked" in str(e):
                # Remove chat from database
                print(f"The {chat} was removed from the database. Reason: Bot was kicked")
                remove_chat(chat)
                continue
            elif "the group chat was deleted" in str(e):
                # Remove chat from database
                print(f"The {chat} was removed from the database. Reason: The group chat was deleted")
                remove_chat(chat)
                continue
            else:
                print(f"An unexpected error occured: {e}")
                continue
