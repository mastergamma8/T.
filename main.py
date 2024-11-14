from aiogram import Bot, Dispatcher, types, F
from handlers.payment import send_invoice_handler, pre_checkout_handler, success_payment_handler, receive_card_number
import asyncio

TOKEN = '7225900512:AAFKfTU5UcE5qTBh6iKmIwlMDFzXnKTGuIw'

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_state = {}
user_star_count = {}
user_balance = {}

# Главное меню
async def show_main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="⭐️Пополнить звездами")],
            [types.KeyboardButton(text="💸Вывод на карту")]
        ],
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

# Обработчик кнопки "💸Вывод на карту"
@dp.message(F.text == "💸Вывод на карту")
async def withdraw_handler(message: types.Message):
    user_id = message.from_user.id
    if user_balance.get(user_id, 0) > 0:
        await message.reply("Введите номер карты для вывода.")
        user_state[user_id] = "waiting_for_card_number"
    else:
        await message.reply("Для вывода на карту сначала пополните баланс.")

# Получение номера карты после успешного пополнения или нажатия на "💸Вывод на карту" с достаточным балансом
@dp.message(lambda message: user_state.get(message.from_user.id) == "waiting_for_card_number")
async def handle_card_number(message: types.Message):
    if message.text == "⬅️Назад":
        await show_main_menu(message)
    else:
        await receive_card_number(message)
        user_state[message.from_user.id] = None

# Обработчики для предварительной проверки и успешной оплаты
dp.pre_checkout_query.register(pre_checkout_handler)
dp.message.register(success_payment_handler, F.successful_payment)

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
