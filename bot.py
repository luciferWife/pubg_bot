import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# 🔹 Загружаем переменные окружения из .env
load_dotenv()

# 🔹 Берем токены из переменных среды
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # ID чата админов (не забудь добавить в Render!)

# 🔹 Проверяем, загружен ли токен
if not TOKEN:
    raise ValueError("❌ Ошибка: BOT_TOKEN не найден! Проверь .env или Render Environment Variables.")

print(f"✅ Бот запускается... (Токен: {TOKEN[:5]}...)")  

# 🔹 Создаем объект бота и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher(storage=MemoryStorage())  # Храним данные регистрации в памяти

# 🔹 Определяем состояния для пошаговой регистрации команды
class RegistrationState(StatesGroup):
    team_name = State()
    player1 = State()
    player2 = State()
    player3 = State()
    player4 = State()
    reserve = State()

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
        "🔥 **Салем, достар! Добро пожаловать в первый в своем роде бот регистрации команд PUBG Mobile KZ!** 🎮\n\n"
        "⚔️ **Горячие кастомки и турниры** от клана **『JT』 Bloody Demons** и **luciferシwife** уже ждут своих героев!\n\n"
        "💡 **Ты готов доказать, что сильнейший?** Жми **/start** и вписывай свое имя в историю боёв! ⚔",
        reply_markup=main_menu()
    )

# 🔹 Обработчик кнопки "🎮 Регистрация команды" (начинаем регистрацию)
@dp.callback_query(lambda c: c.data == "register")
@dp.message(Command("register"))
async def register_team(event: types.Message | types.CallbackQuery, state: FSMContext):
    message = event if isinstance(event, types.Message) else event.message
    await message.answer("🏆 Введите название вашей команды:")
    await state.set_state(RegistrationState.team_name)

# 🔹 Шаг 1: Получаем название команды
@dp.message(RegistrationState.team_name)
async def process_team_name(message: types.Message, state: FSMContext):
    await state.update_data(team_name=message.text)
    await message.answer("👤 Введите имя первого игрока:")
    await state.set_state(RegistrationState.player1)

# 🔹 Шаг 2: Получаем игрока 1
@dp.message(RegistrationState.player1)
async def process_player1(message: types.Message, state: FSMContext):
    await state.update_data(player1=message.text)
    await message.answer("👤 Введите имя второго игрока:")
    await state.set_state(RegistrationState.player2)

# 🔹 Шаг 3: Получаем игрока 2
@dp.message(RegistrationState.player2)
async def process_player2(message: types.Message, state: FSMContext):
    await state.update_data(player2=message.text)
    await message.answer("👤 Введите имя третьего игрока:")
    await state.set_state(RegistrationState.player3)

# 🔹 Шаг 4: Получаем игрока 3
@dp.message(RegistrationState.player3)
async def process_player3(message: types.Message, state: FSMContext):
    await state.update_data(player3=message.text)
    await message.answer("👤 Введите имя четвертого игрока:")
    await state.set_state(RegistrationState.player4)

# 🔹 Шаг 5: Получаем игрока 4
@dp.message(RegistrationState.player4)
async def process_player4(message: types.Message, state: FSMContext):
    await state.update_data(player4=message.text)
    await message.answer("👥 Введите имя запасного игрока (если нет, напишите 'нет'):")
    await state.set_state(RegistrationState.reserve)

# 🔹 Шаг 6: Получаем запасного игрока и завершаем регистрацию
@dp.message(RegistrationState.reserve)
async def process_reserve(message: types.Message, state: FSMContext):
    data = await state.get_data()
    reserve_player = message.text if message.text.lower() != "нет" else "Нет"

    confirmation_text = (
        f"✅ **Регистрация завершена!** ✅\n\n"
        f"🏆 **Название команды:** {data['team_name']}\n"
        f"👤 **Игроки:**\n"
        f"  1️⃣ {data['player1']}\n"
        f"  2️⃣ {data['player2']}\n"
        f"  3️⃣ {data['player3']}\n"
        f"  4️⃣ {data['player4']}\n"
        f"👥 **Запасной игрок:** {reserve_player}\n\n"
        f"📢 Ожидайте подтверждения от администрации!"
    )

    await message.answer(confirmation_text)
    
    if ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, f"🚀 **Новая заявка на регистрацию!**\n\n{confirmation_text}")

    await state.clear()

# 🔹 Запуск бота
async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot, skip_updates=True)  # skip_updates=True помогает избежать конфликтов

if __name__ == "__main__":
    asyncio.run(main())
