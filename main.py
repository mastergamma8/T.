from aiogram import Bot, Dispatcher, types, F
from handlers.payment import send_invoice_handler, pre_checkout_handler, success_payment_handler
from state import user_state, user_star_count, user_balance
import asyncio

TOKEN = '7225900512:AAFKfTU5UcE5qTBh6iKmIwlMDFzXnKTGuIw'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
async def show_main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="⭐️Пополнить звездами")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.reply("Выберите опцию", reply_markup=keyboard)
    user_state[message.from_user.id] = None

# Команда /start
@dp.message(F.text == "/start")
async def start_command_handler(message: types.Message):
    await show_main_menu(message)

# Обработчик кнопки "⭐️Пополнить звездами"
@dp.message(F.text == "⭐️Пополнить звездами")
async def donate_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="⬅️Назад")]],
        resize_keyboard=True
    )
    await message.reply("Введите количество звезд, которое вы хотите отправить", reply_markup=keyboard)
    user_state[message.from_user.id] = "waiting_for_star_count"

# Получение количества звезд
@dp.message(lambda message: user_state.get(message.from_user.id) == "waiting_for_star_count")
async def receive_star_count(message: types.Message):
    if message.text == "⬅️Назад":
        await show_main_menu(message)
    else:
        try:
            star_count = int(message.text)
            if star_count <= 0:
                await message.reply("Пожалуйста, введите положительное число.")
                return
            user_star_count[message.from_user.id] = star_count
            await send_invoice_handler(message, star_count)
            user_state[message.from_user.id] = None
        except ValueError:
            await message.reply("Пожалуйста, введите корректное количество звезд.")

# Обработчики для предварительной проверки и успешной оплаты
dp.pre_checkout_query.register(pre_checkout_handler)
dp.message.register(success_payment_handler, F.successful_payment)

# Обработчик для получения номера карты
@dp.message(lambda message: user_state.get(message.from_user.id) == "waiting_for_card_number")
async def receive_card_number(message: types.Message):
    card_number = message.text.strip()  # Получаем введённый номер карты
    if len(card_number) < 16:  # Проверка на длину номера карты
        await message.reply("Пожалуйста, введите корректный номер карты.")
    else:
        # Логика обработки номера карты (например, создание заявки)
        await message.reply("Заявка успешно создана, ожидайте.")
        # Сбрасываем состояние пользователя
        user_state[message.from_user.id] = None  # Состояние сбрасывается после ввода карты

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
