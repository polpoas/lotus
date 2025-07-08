import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8008348062:AAENy4fVc-TuHOLeKONbBKmcSW2RqD644Gs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Капча словарь
captcha_answers = {}

@dp.message(Command("start"))
async def start_handler(message: Message):
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    answer = num1 + num2
    captcha_answers[message.from_user.id] = answer

    await message.answer(f"Подтвердите, что вы человек: сколько будет {num1} + {num2}?")

@dp.message()
async def captcha_check(message: Message):
    user_id = message.from_user.id
    if user_id not in captcha_answers:
        await message.answer("Сначала напишите /start.")
        return

    try:
        user_answer = int(message.text)
        if user_answer == captcha_answers[user_id]:
            del captcha_answers[user_id]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🌸 Цветочный | VCC & BA",
                    url="https://t.me/+NakqaGGxyew3ZTlk"
                )]
            ])
            await message.answer("Проверка пройдена ✅", reply_markup=keyboard)
        else:
            await message.answer("Неправильно. Напишите /start ещё раз.")
    except ValueError:
        await message.answer("Введите число.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import random
    asyncio.run(main())
