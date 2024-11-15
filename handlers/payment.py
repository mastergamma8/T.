from aiogram.types import LabeledPrice, Message, PreCheckoutQuery
from botlogic.keyboards.payment_keyboard import payment_keyboard
from state import user_state, user_star_count, user_balance

# Обработчик отправки инвойса
async def send_invoice_handler(message: Message, star_count: int):
    price_per_star = 1
    total_amount = star_count * price_per_star
    prices = [LabeledPrice(label="Звезды", amount=total_amount)]
    
    await message.answer_invoice(
        title="Пополнение счета",
        description=f"Пополнить счет на {star_count} звёзд!",
        prices=prices,
        provider_token="your_provider_token_here",
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_keyboard(),
    )

# Обработчик предварительной проверки платежа
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

# Обработчик успешного платежа
async def success_payment_handler(message: Message):
    user_id = message.from_user.id
    star_count = user_star_count.get(user_id, 0)
    user_balance[user_id] = user_balance.get(user_id, 0) + star_count
    await message.reply("Вы успешно пополнили баланс! Теперь введите номер карты для вывода.")
    user_state[user_id] = "waiting_for_card_number"  # Обновляем состояние на "ожидание номера карты"
