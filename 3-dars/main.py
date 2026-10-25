# ============================================================
#  3-DARS — Inline klaviatura va callback
#  Maqsad: tugmalar bilan katalog aylansin, chat toza qolsin
#
#  YOZISH TARTIBI:
#    1-bosqich: kategoriyalar_kb()  -> inline tugmalar
#    2-bosqich: @dp.callback_query  -> tugma bosilishini tutish
#    3-bosqich: mahsulotlar_kb()    -> ichkariga kirish
#    4-bosqich: mahsulot_kb()       -> mahsulot kartasi + "Orqaga"
#
#  ENG MUHIM QOIDA: har bir callback handler oxirida
#                   await call.answer()  bo'lishi SHART.
#                   Unutsangiz — tugmada soat aylanaveradi.
# ============================================================

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from data import CATEGORIES, mahsulot_top, narx

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

dp = Dispatcher()


# ---------- 1-bosqich ----------
def kategoriyalar_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for kalit, kategoriya in CATEGORIES.items():
        # callback_data — tugma bosilganda bizga qaytadigan SATR (max 64 bayt)
        kb.button(text=kategoriya["nom"], callback_data=f"kat:{kalit}")
    kb.adjust(2)
    return kb.as_markup()


# ---------- 3-bosqich ----------
def mahsulotlar_kb(kalit: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for m in CATEGORIES[kalit]["mahsulotlar"]:
        kb.button(text=f"{m['nom']} — {narx(m['narx'])}", callback_data=f"mah:{m['id']}")
    kb.adjust(1)
    kb.row()
    kb.button(text="🔙 Kategoriyalar", callback_data="orqaga")
    return kb.as_markup()


# ---------- 4-bosqich ----------
def mahsulot_kb(kalit: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Savatga qo'shish", callback_data="savatga")
    kb.button(text="🔙 Orqaga", callback_data=f"kat:{kalit}")
    kb.adjust(1)
    return kb.as_markup()


@dp.message(CommandStart())
@dp.message(Command("menyu"))
async def start(message: Message):
    await message.answer("🍽 <b>Menyu</b>\n\nKategoriyani tanlang:", reply_markup=kategoriyalar_kb())


# ---------- 2-bosqich ----------
@dp.callback_query(F.data == "orqaga")
async def orqaga(call: CallbackQuery):
    # edit_text — YANGI xabar yubormaydi, borini o'zgartiradi. Chat toza qoladi.
    await call.message.edit_text("🍽 <b>Menyu</b>\n\nKategoriyani tanlang:",
                                 reply_markup=kategoriyalar_kb())
    await call.answer()


@dp.callback_query(F.data.startswith("kat:"))
async def kategoriya(call: CallbackQuery):
    kalit = call.data.split(":")[1]        # "kat:burger" -> "burger"
    kategoriya = CATEGORIES.get(kalit)
    if not kategoriya:
        return await call.answer("Bunday kategoriya yo'q", show_alert=True)

    await call.message.edit_text(f"<b>{kategoriya['nom']}</b>\n\nMahsulotni tanlang:",
                                 reply_markup=mahsulotlar_kb(kalit))
    await call.answer()


@dp.callback_query(F.data.startswith("mah:"))
async def mahsulot(call: CallbackQuery):
    mahsulot_id = int(call.data.split(":")[1])
    m = mahsulot_top(mahsulot_id)
    if not m:
        return await call.answer("Mahsulot topilmadi", show_alert=True)

    # mahsulot qaysi kategoriyada ekanini topamiz (orqaga qaytish uchun)
    kalit = next(k for k, v in CATEGORIES.items()
                 if any(x["id"] == mahsulot_id for x in v["mahsulotlar"]))

    await call.message.edit_text(
        f"<b>{m['nom']}</b>\n\n{m['tavsif']}\n\n💰 Narxi: <b>{narx(m['narx'])}</b>",
        reply_markup=mahsulot_kb(kalit),
    )
    await call.answer()


@dp.callback_query(F.data == "savatga")
async def savatga(call: CallbackQuery):
    # show_alert=True — o'rtada oyna chiqadi. False bo'lsa — yuqorida kichik yozuv.
    await call.answer("✅ Savatga qo'shildi!\n\n(Savatni 4-darsda yozamiz)", show_alert=True)


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.info("Bot ishga tushdi: @%s", (await bot.get_me()).username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
