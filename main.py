from aiogram import Bot, Dispatcher, types, F
from handlers import payment  # Импортируем обработчики для платежей
import asyncio

TOKEN = '7596590431:AAEpLzcjwyar1hOqR1jGEnPY_ZA6YORzP-w'  # Замените на ваш токен бота

# Создаем экземпляр бота
bot = Bot(token=TOKEN)

# Создаем экземпляр диспетчера
dp = Dispatcher()

# Обработчик для команды /start
@dp.message(F.text == "/start")
async def start_command_handler(message: types.Message):
    await message.reply("Привет! Я ваш бот. Чем могу помочь? /donate /paysupport")

# Регистрируем обработчики платежей
dp.message.register(payment.send_invoice_handler, F.text == "/donate")
dp.pre_checkout_query.register(payment.pre_checkout_handler)
dp.message.register(payment.success_payment_handler, F.successful_payment)
dp.message.register(payment.pay_support_handler, F.text == "/paysupport")

async def main():
    # Привязываем диспетчер к боту и запускаем polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    # Запуск основной функции
    asyncio.run(main())