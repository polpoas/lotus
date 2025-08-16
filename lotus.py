import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    FSInputFile,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

API_TOKEN = "8008348062:AAENy4fVc-TuHOLeKONbBKmcSW2RqD644Gs"
ADMIN_ID = 7922633226  # Замени на свой ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

captcha_answers = {}
USERS_FILE = "users.txt"

# Функции для работы с пользователями
def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return [int(line.strip()) for line in f if line.strip().isdigit()]
    except FileNotFoundError:
        return []

def save_users(user_ids):
    with open(USERS_FILE, 'w') as f:
        for user_id in set(user_ids):  # Удаляем дубликаты
            f.write(f"{user_id}\n")

def add_users(new_ids):
    existing = load_users()
    updated = list(set(existing + [int(i) for i in new_ids if str(i).isdigit()]))
    save_users(updated)
    return len(updated) - len(existing)

# Основные хэндлеры
@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    users = load_users()
    
    if user_id not in users:
        add_users([user_id])
    
    image_path = "welcome.jpg"
    photo = FSInputFile(image_path)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👉 Continue", callback_data="captcha")]
        ]
    )

    await message.answer_photo(
        photo,
        caption="🌸 Welcome to Lotus | VCC & BA",
        reply_markup=keyboard
    )

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Access denied")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Add Users", callback_data="add_users")],
        [InlineKeyboardButton(text="📊 Stats", callback_data="stats")],
        [InlineKeyboardButton(text="📨 Broadcast", callback_data="broadcast")]
    ])
    
    await message.answer("Admin Panel:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "add_users")
async def ask_for_ids(callback: CallbackQuery):
    await callback.message.answer(
        "Send user IDs separated by commas, spaces or new lines:"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "stats")
async def show_stats(callback: CallbackQuery):
    users = load_users()
    await callback.message.answer(f"📊 Total users: {len(users)}")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "broadcast")
async def ask_for_broadcast(callback: CallbackQuery):
    await callback.message.answer(
        "Send the message you want to broadcast to all users:"
    )
    await callback.answer()

# Обработка текста от админа
@dp.message(lambda m: m.from_user.id == ADMIN_ID)
async def handle_admin_text(message: Message):
    if message.reply_to_message and "user IDs" in message.reply_to_message.text:
        new_ids = [int(i) for i in message.text.replace(',', ' ').split() if i.isdigit()]
        added = add_users(new_ids)
        await message.answer(f"✅ Added {added} new users")
    
    elif message.reply_to_message and "broadcast" in message.reply_to_message.text:
        users = load_users()
        success = 0
        for user_id in users:
            try:
                await bot.send_message(user_id, message.text)
                success += 1
                await asyncio.sleep(0.1)  # Anti-flood
            except:
                continue
        await message.answer(f"📨 Sent to {success}/{len(users)} users")

# Остальные хэндлеры (капча и т.д.) остаются без изменений
@dp.callback_query(lambda c: c.data == "captcha")
async def ask_captcha(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    answer = num1 + num2
    captcha_answers[user_id] = answer

    await callback_query.message.answer(
        f"Confirm you're human: how much is {num1} + {num2}?"
    )
    await callback_query.answer()

@dp.message()
async def captcha_check(message: Message):
    user_id = message.from_user.id
    if user_id not in captcha_answers:
        await message.answer("First, enter /start.")
        return

    try:
        user_answer = int(message.text)
        if user_answer == captcha_answers[user_id]:
            del captcha_answers[user_id]

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🌸 Lotus | VCC & BA",
                    url="https://t.me/+0j1ZYHB7E_g4YzJi"
                )]
            ])

            image_path = "welcome.jpg"
            photo = FSInputFile(image_path)

            await message.answer_photo(
                photo,
                caption=(
                    "🎉 Glad to see you on our channel!\n\n"  
                    "We are back in the big market, starting work and ready to provide you with the best on the market "  
                    "services for VCC & BA registration!\n\n"  
                    "Go to the channel and find a solution for your tasks!"  
                ),
                reply_markup=keyboard
            )
        else:
            await message.answer("❌ Wrong. Try again: /start")
    except ValueError:
        await message.answer("Please enter the number.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Создаем файл users.txt если его нет
    try:
        open(USERS_FILE, 'x').close()
    except FileExistsError:
        pass
    
    asyncio.run(main())
