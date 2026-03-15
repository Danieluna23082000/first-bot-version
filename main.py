import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")
PDF_PATH = "presentation.pdf"
TG_LINK = "https://t.me/danyaytb"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}" if BASE_URL else None

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
async def get_pdf_handler(callback: CallbackQuery):
    pdf = FSInputFile(PDF_PATH)
    await callback.message.answer_document(
        document=pdf,
        caption=(
            "Ниже — PDF с подходом к работе, результатами и форматами сотрудничества.\n\n"
            "Если будет актуально, напиши в личку — разберем твой YouTube и покажем точки роста."
        ),
        reply_markup=after_pdf_keyboard(),
    )
    await callback.answer()


async def on_startup(bot: Bot):
    if WEBHOOK_URL:
        await bot.set_webhook(
            WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
        )


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


def main():
    logging.basicConfig(level=logging.INFO)

    if not BOT_TOKEN:
        raise ValueError("Не задан BOT_TOKEN")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    port = int(os.getenv("PORT", "8000"))
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
