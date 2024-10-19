from aiogram import Bot, F, types, Router
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

from app.constants.wrap import SUBSCRIPTION_DESCRIPTION
sub_router = Router()

@sub_router.message(Command(commands=['subscription']))
async def subscription(msg: types.Message, bot: Bot):
    chat_id = msg.chat.id

    await bot.send_invoice(chat_id,
                           title="Premium Subscription",
                           description=SUBSCRIPTION_DESCRIPTION,
                           payload="private",
                           currency="XTR",
                           prices=[LabeledPrice(label='XTR', amount=1)],
                           )

@sub_router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@sub_router.message(F.successful_payment)
async def successful_payment(msg: types.Message):
    await msg.bot.refund_star_payment(msg.from_user.id,
                                      msg.successful_payment.telegram_payment_charge_id)
    
    await msg.reply("test subscription was successful")