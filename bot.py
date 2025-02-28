from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN, ADMIN_CHAT_ID
from database import register_team

from aiogram.client.default import DefaultBotProperties
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="Markdown")) # Обновлённый код для Render
dp = Dispatcher(storage=MemoryStorage())

# Главное меню
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Правила")],
            [KeyboardButton(text="🎮 Регистрация команды")],
        ],
        resize_keyboard=True
    )

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("🔥 Добро пожаловать в бота регистрации команд PUBG Mobile KZ!\nВыберите действие:", reply_markup=main_menu())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
