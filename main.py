from aiogram import Bot, Dispatcher, types, F
from handlers.payment import send_invoice_handler, pre_checkout_handler, success_payment_handler
import asyncio

TOKEN = '7225900512:AAFKfTU5UcE5qTBh6iKmIwlMDFzXnKTGuIw'  # Замените на ваш токен бота

# Создаем экземпляр бота
bot = Bot(token=TOKEN)

# Создаем экземпляр диспетчера
dp = Dispatcher()

# Глобальная переменная для хранения состояния пользователей
user_state = {}
user_star_count = {}

# Функция для возвращения в главное меню
async def show_main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="⭐️Пополнить звездами")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    # Если пользователь отправил звезды, добавляем кнопку "Вывод на карту"
    if user_star_count.get(message.from_user.id):
        keyboard.keyboard.append([types.KeyboardButton(text="💸Вывод на карту")])
    await message.reply("Выберите опцию", reply_markup=keyboard)
    user_state[message.from_user.id] = None  # Сброс состояния
# Обработчик для команды /start
@dp.message(F.text == "/start")
async def start_command_handler(message: types.Message):
    await show_main_menu(message)

# Обработчик для кнопки "⭐️Пополнить звездами"
@dp.message(F.text == "⭐️Пополнить звездами")
async def donate_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="⬅️Назад")]],
        resize_keyboard=True
    )
    await message.reply("Введите количество звезд, которое вы хотите отправить", reply_markup=keyboard)
    user_state[message.from_user.id] = "waiting_for_star_count"

# Обработчик для ввода количества звезд
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
            user_state[message.from_user.id] = None  # Сбрасываем состояние после отправки инвойса
            await show_main_menu(message)  # Обновляем меню, чтобы появилась кнопка вывода на карту
        except ValueError:
            await message.reply("Пожалуйста, введите корректное количество звезд.")

# Обработчик для предварительной проверки перед оплатой
dp.pre_checkout_query.register(pre_checkout_handler)

# Обработчик успешной оплаты
@dp.message.register(success_payment_handler, F.successful_payment)
async def handle_successful_payment(message: types.Message):
    # Сохраняем, что пользователь оплатил определенное количество звезд
    user_star_count[message.from_user.id] += message.successful_payment.total_amount  # или просто установите количество звезд, если не используется сумма
    await show_main_menu(message)  # Обновляем главное меню и добавляем кнопку "Вывод на карту"

# Обработчик для кнопки "💸Вывод на карту"
@dp.message(F.text == "💸Вывод на карту")
async def withdraw_handler(message: types.Message):
    if not user_star_count.get(message.from_user.id):  # Проверка, отправил ли пользователь звезды
        await message.reply("Сначала пополните баланс звездами, чтобы воспользоваться выводом на карту.")
        return
    user_state[message.from_user.id] = "waiting_for_card_number"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="⬅️Назад")]],
        resize_keyboard=True
    )
    await message.reply("Введите номер карты", reply_markup=keyboard)

# Обработчик для ввода номера карты
@dp.message(lambda message: user_state.get(message.from_user.id) == "waiting_for_card_number")
async def receive_card_number(message: types.Message):
    if message.text == "⬅️Назад":
        await show_main_menu(message)
    else:
        await message.reply("Заявка успешно создана, Ожидайте.")
        user_state[message.from_user.id] = None  # Сбрасываем состояние после создания заявки

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
