from aiogram.types import LabeledPrice, Message, PreCheckoutQuery
from botlogic.keyboards.payment_keyboard import payment_keyboard

# Обработчик отправки инвойса
async def send_invoice_handler(message: Message, star_count: int):
    # Цена за 1 звезду = 100 единиц валюты XTR
    price_per_star = 1
    total_amount = star_count * price_per_star  # Рассчитываем общую сумму

    # Создаем список цен для инвойса
    prices = [LabeledPrice(label="Звезды", amount=total_amount)]

    # Отправляем инвойс пользователю
    await message.answer_invoice(
        title="Пополнение счета",
        description=f"Пополнить счет на {star_count} звёзд!",
        prices=prices,
        provider_token="your_provider_token_here",  # Замените на ваш provider_token
        payload="channel_support",
        currency="XTR",
        reply_markup=payment_keyboard(),
    )

# Обработчик предварительной проверки платежа
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    # Подтверждаем, что все ок для платежа
    await pre_checkout_query.answer(ok=True)

# Обработчик успешного платежа
async def success_payment_handler(message: Message):
    # Сообщение об успешном пополнении и запрос на ввод номера карты
    await message.reply("Вы успешно пополнили баланс! Теперь введите номер карты для вывода.")

# Обработчик для получения номера карты
async def receive_card_number(message: Message):
    # Сообщение о создании заявки
    await message.reply("Заявка успешно создана, ожидайте.")
