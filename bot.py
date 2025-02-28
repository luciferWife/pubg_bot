import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# 🔹 Загружаем переменные окружения из .env
load_dotenv()

# 🔹 Берем токен бота из переменных среды
TOKEN = os.getenv("BOT_TOKEN")

# 🔹 Проверяем, загружен ли токен
if not TOKEN:
    raise ValueError("❌ Ошибка: BOT_TOKEN не найден! Проверь .env или Render Environment Variables.")

print(f"✅ Бот запускается... (Токен: {TOKEN[:5]}...)")  # Выводит первые 5 символов токена

# 🔹 Создаем объект бота и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

# 🔹 Главное меню с кнопками
def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Правила", callback_data="rules")],
        [InlineKeyboardButton(text="🎮 Регистрация команды", callback_data="register")],
        [InlineKeyboardButton(text="📢 Наши соцсети", callback_data="socials")]
    ])
    return keyboard

# 🔹 Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🔥 **Салем, достар! Добро пожаловать в первый в своем роде бот регистрации команд PUBG Mobile !** 🎮\n\n"
        "⚔️ **Горячие кастомки и турниры** от клана **『JT』 Bloody Demons** и **luciferシwife** уже ждут своих героев!\n\n"
        "💡 **Ты готов доказать, что сильнейший?** Жми **/start** и вписывай свое имя в историю боёв! 💀🔥",
        reply_markup=main_menu()
    )

# 🔹 Обработчик кнопки "📜 Правила"
@dp.callback_query(lambda c: c.data == "rules")
async def rules_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📜 **Вот правила турнира:**\n"
        "1️⃣ **Соблюдайте честную игру** - никаких читов и запрещённых программ!\n"
        "2️⃣ **Запрещены оскорбления и токсичное поведение**.\n"
        "3️⃣ **Каждый игрок может участвовать только в одной команде**.\n\n"
        "⚠️ Нарушение правил приведёт к дисквалификации!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()

# 🔹 Обработчик кнопки "🎮 Регистрация команды"
@dp.callback_query(lambda c: c.data == "register")
async def register_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎮 **Для регистрации команды отправьте заявку по форме:**\n\n"
        "🏆 *Название команды:* ...\n"
        "👤 *Игрок 1:* ...\n"
        "👤 *Игрок 2:* ...\n"
        "👤 *Игрок 3:* ...\n"
        "👤 *Игрок 4:* ...\n\n"
        "✅ *После регистрации ожидайте подтверждения от администрации!*",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()

# 🔹 Обработчик кнопки "📢 Наши соцсети"
@dp.callback_query(lambda c: c.data == "socials")
async def socials_callback(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📷 TikTok стримы", url="https://www.tiktok.com/@lucifer__wife")],
        [InlineKeyboardButton(text="📢 Telegram канал", url="https://t.me/jtpubg")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")]
    ])
    await callback.message.edit_text("📢 **Наши соцсети:**", reply_markup=keyboard)
    await callback.answer()

# 🔹 Обработчик кнопки "⬅️ Назад в меню"
@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔥 **Салем, достар! Добро пожаловать в первый в своем роде бот регистрации команд PUBG Mobile KZ!** 🎮\n\n"
        "⚔️ **Горячие кастомки и турниры** от клана **『JT』 Bloody Demons** и **luciferシwife** уже ждут своих героев!\n\n"
        "💡 **Ты готов доказать, что сильнейший?** Жми **/start** и вписывай свое имя в историю боёв! 💀🔥",
        reply_markup=main_menu()
    )
    await callback.answer()

# 🔹 Обработчик неизвестных команд
@dp.message()
async def unknown_command(message: types.Message):
    await message.reply("❌ *Неизвестная команда.* Используйте /start для меню.")

# 🔹 Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
