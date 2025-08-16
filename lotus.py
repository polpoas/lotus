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
            [InlineKeyboardButton(text="👉 Continue", callback_data="captcha")]
        ]
    )

    await message.answer_photo(
        photo,
        caption="🌸 Welcome to Lotus | VCC & BA",
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
    asyncio.run(main())




