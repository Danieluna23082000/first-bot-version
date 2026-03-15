import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")
PDF_PATH = "presentation.pdf"
TG_LINK = "https://t.me/danyaytb"

dp = Dispatcher()

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Получить PDF", callback_data="get_pdf")]
        ]
    )

def after_pdf_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Написать в личку", url=TG_LINK)]
        ]
    )

@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "Привет.\n\n"
        "Здесь — короткая презентация по YouTube: как канал может работать "
        "на охваты, доверие и заявки.\n\n"
        "Нажми кнопку ниже, чтобы получить PDF."
    )
    await message.answer(text, reply_markup=start_keyboard())

@dp.callback_query(F.data == "get_pdf")
async def get_pdf_handler(callback):
    pdf = FSInputFile(PDF_PATH)
    await callback.message.answer_document(
        document=pdf,
        caption=(
            "Ниже — PDF с подходом к работе, результатами и форматами сотрудничества.\n\n"
            "Если будет актуально, напиши в личку — разберем твой YouTube и покажем точки роста."
        ),
        reply_markup=after_pdf_keyboard()
    )
    await callback.answer()

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())