# ============================================================
#  2-DARS — Reply klaviatura va menyu
#  Maqsad: pastda doimiy tugmalar chiqsin
#
#  YOZISH TARTIBI:
#    1-bosqich: data.py faylini yozing (mahsulotlar ro'yxati)
#    2-bosqich: bosh_menyu() funksiyasi — klaviatura yasaydi
#    3-bosqich: start() da reply_markup=bosh_menyu() qo'shing
#    4-bosqich: har bir tugma uchun handler yozing
#
#  YANGI TUSHUNCHA: F.text == "🍽 Menyu"  — tugma bosilganda
#                   oddiy MATN keladi, shuni tutamiz.
# ============================================================

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

from data import CATEGORIES, narx

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

dp = Dispatcher()

BTN_MENYU = "🍽 Menyu"
BTN_SAVAT = "🧺 Savat"
BTN_PROFIL = "👤 Profil"
BTN_YORDAM = "ℹ️ Yordam"


# ---------- 2-bosqich ----------
def bosh_menyu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(KeyboardButton(text=BTN_MENYU), KeyboardButton(text=BTN_SAVAT))
    kb.row(KeyboardButton(text=BTN_PROFIL), KeyboardButton(text=BTN_YORDAM))
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Bo'limni tanlang…")


# ---------- 3-bosqich ----------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Salom, <b>{message.from_user.full_name}</b>!\n\nQuyidagi menyudan tanlang 👇",
        reply_markup=bosh_menyu(),
    )


# ---------- 4-bosqich ----------
@dp.message(F.text == BTN_MENYU)
async def menyu(message: Message):
    qatorlar = []
    for kalit, kategoriya in CATEGORIES.items():
        qatorlar.append(f"\n<b>{kategoriya['nom']}</b>")
        for m in kategoriya["mahsulotlar"]:
            qatorlar.append(f"  • {m['nom']} — {narx(m['narx'])}")
    await message.answer("\n".join(qatorlar))


@dp.message(F.text == BTN_SAVAT)
async def savat(message: Message):
    await message.answer("🧺 Savatingiz bo'sh.\n\n<i>Savatni 4-darsda yozamiz.</i>")


@dp.message(F.text == BTN_PROFIL)
async def profil(message: Message):
    u = message.from_user
    await message.answer(
        f"👤 <b>Profil</b>\n\n"
        f"Ism: <b>{u.full_name}</b>\n"
        f"Username: @{u.username or '—'}\n"
        f"ID: <code>{u.id}</code>"
        f"Jami{ u }"
    )


@dp.message(F.text == BTN_YORDAM)
async def yordam(message: Message):
    await message.answer("Menyudan tanlang yoki /start yozing.")


# Tanilmagan matn — ENG OXIRIDA
@dp.message(F.text)
async def boshqa(message: Message):
    await message.answer("Tushunmadim. Menyudan tanlang 👇", reply_markup=bosh_menyu())


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.info("Bot ishga tushdi: @%s", (await bot.get_me()).username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
