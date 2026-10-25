# ============================================================
#  1-DARS — Birinchi bot
#  Maqsad: bot Telegramda javob bersin
#
#  YOZISH TARTIBI (o'quvchi shu tartibda yozadi):
#    1-bosqich: importlar + main() + ishga tushirish  -> bot ishlaydi, lekin jim
#    2-bosqich: start() handler                        -> /start ga javob beradi
#    3-bosqich: help_cmd() handler                     -> /help ga javob beradi
#    4-bosqich: echo() handler                         -> hamma narsani takrorlaydi
#
#  ISHGA TUSHIRISH:  python main.py
# ============================================================

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

dp = Dispatcher()


# ---------- 2-bosqich ----------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Salom, <b>{message.from_user.full_name}</b>!\n\n"
        f"Men birinchi botman. /help yozing."
    )


# ---------- 3-bosqich ----------
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "<b>Buyruqlar:</b>\n"
        "/start — boshlash\n"
        "/help — yordam\n\n"
        "Yoki oddiy matn yozing — men takrorlayman."
    )


# ---------- 4-bosqich ----------
# DIQQAT: bu handler ENG OXIRIDA turishi shart!
# Yuqoriga ko'chiring — /start ishlamay qoladi. Sinab ko'ring.
@dp.message(F.text)
async def echo(message: Message):
    await message.answer(f"Siz yozdingiz: {message.text}")


# ---------- 1-bosqich ----------
async def main():
    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    me = await bot.get_me()
    logging.info("Bot ishga tushdi: @%s", me.username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
