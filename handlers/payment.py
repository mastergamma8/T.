from aiogram.types import LabeledPrice, Message, PreCheckoutQuery
from botlogic.keyboards.payment_keyboard import payment_keyboard

async def send_invoice_handler(message: Message, star_count: int):
    prices = [LabeledPrice(label="Звезды", amount=star_count * 100)]
    await message.answer_invoice(
        title="Пополнение счета",
        description=f"Пополнить счет на {star_count} звёзд!",
        prices=prices,
        provider_token="",  # Добавьте ваш provider_token
        payload="channel_support",
        currency="XTR",  # Используйте правильную валюту
        reply_markup=payment_keyboard(),
    )

async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

async def success_payment_handler(message: Message):
    await message.answer(text="Вы успешно пополнили баланс")
