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

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

captcha_answers = {}

@dp.message(Command("start"))
async def start_handler(message: Message):
    image_path = "welcome.jpg"
    photo = FSInputFile(image_path)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👉 Далее", callback_data="captcha")]
        ]
    )

    await message.answer_photo(
        photo,
        caption="🌸 Вас приветствует Цветочный | VCC & BA",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "captcha")
async def ask_captcha(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    answer = num1 + num2
    captcha_answers[user_id] = answer

    await callback_query.message.answer(
        f"Подтвердите, что вы человек: сколько будет {num1} + {num2}?"
    )
    await callback_query.answer()

@dp.message()
async def captcha_check(message: Message):
    user_id = message.from_user.id
    if user_id not in captcha_answers:
        await message.answer("Сначала введите /start.")
        return

    try:
        user_answer = int(message.text)
        if user_answer == captcha_answers[user_id]:
            del captcha_answers[user_id]

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🌸 Цветочный | VCC & BA",
                    url="https://t.me/+FKEQoNMlSOI3ZmNk"
                )]
            ])

            image_path = "welcome.jpg"
            photo = FSInputFile(image_path)

            await message.answer_photo(
                photo,
                caption=(
                    "🎉 Рады видеть на нашем канале!\n\n"
                    "Мы вернулись на большой рынок, приступаем к работе и готовы предоставлять для вас лучшие на рынке "
                    "услуги по регистрации VCC & BA!\n\n"
                    "Переходите на канал и найдите для себя решение своих задач!"
                ),
                reply_markup=keyboard
            )
        else:
            await message.answer("❌ Неправильно. Попробуйте снова: /start")
    except ValueError:
        await message.answer("Введите число, пожалуйста.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
