from aiogram import Bot, Dispatcher, types, F
from handlers.payment import send_invoice_handler, pre_checkout_handler, success_payment_handler
import asyncio

TOKEN = '7596590431:AAEpLzcjwyar1hOqR1jGEnPY_ZA6YORzP-w'  # Замените на ваш токен бота

# Создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем глобальную переменную для хранения количества звезд
user_star_count = {}

# Обработчик для команды /start
@dp.message(F.text == "/start")
async def start_command_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("⭐️Пополнить звездами"),
        types.KeyboardButton("💸Вывод на карту")
    )
    await message.reply("Привет! Я ваш бот. Чем могу помочь?", reply_markup=keyboard)

# Обработчик для кнопки "⭐️Пополнить звездами"
@dp.message(F.text == "⭐️Пополнить звездами")
async def donate_handler(message: types.Message):
    await message.reply("Введите количество звезд, которое вы хотите отправить.")
    user_star_count[message.from_user.id] = None

# Обработчик для получения количества звезд
@dp.message(lambda message: message.from_user.id in user_star_count and user_star_count[message.from_user.id] is None)
async def receive_star_count(message: types.Message):
    try:
        star_count = int(message.text)
        if star_count <= 0:
            await message.reply("Пожалуйста, введите положительное число.")
            return
        user_star_count[message.from_user.id] = star_count
        await send_invoice_handler(message, star_count)
    except ValueError:
        await message.reply("Пожалуйста, введите корректное количество звезд.")

# Обработчик для предварительной проверки перед оплатой
dp.pre_checkout_query.register(pre_checkout_handler)

# Обработчик успешной оплаты
dp.message.register(success_payment_handler, F.successful_payment)

# Обработчик для кнопки "💸Вывод на карту"
@dp.message(F.text == "💸Вывод на карту")
async def withdraw_handler(message: types.Message):
    await message.reply("Заявка успешно создана, Ожидайте.")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
