# 1-dars — Birinchi bot

| | |
|---|---|
| **Davomiyligi** | 70 daqiqa |
| **Oldindan kerak** | Python 3.11+, Telegram akkaunti |
| **Tayyor kod** | `darslar/1-dars/` |
| **Oldingi darsdan farqi** | — (birinchi dars) |

## Maqsad

Har bir o'quvchi o'z Telegram botini yaratib, unga javob beradigan qilib ishga tushiradi.

## Vazifalar — dars oxirida o'quvchi buni qila oladi

- [ ] BotFather'dan bot yaratib, token oladi
- [ ] Virtual muhit yaratadi va aiogram o'rnatadi
- [ ] Tokenni `.env` faylida xavfsiz saqlaydi
- [ ] `/start` va `/help` buyruqlariga javob yozadi
- [ ] Har qanday matnni takrorlaydigan handler yozadi
- [ ] **Handler tartibi nima uchun muhimligini tushuntirib bera oladi**

## Yangi tushunchalar

`Bot` · `Dispatcher` · handler · filtr · dekorator · `async` / `await` · handler tartibi

## Yaratiladigan fayllar

```
mening_botim/
├── main.py          ← butun kod shu yerda
├── .env             ← token
└── .gitignore
```

---
## Dars maqsadi

O'quvchi shu uchtasini tushunib ketsin:

1. Bot — sehr emas, **oddiy HTTP dastur**
2. `Bot` va `Dispatcher` — ikki xil narsa, ikki xil vazifa
3. **Handler tartibi muhim** — birinchi mos kelgani g'olib

---

## 1-qism. Tahta oldida (10 daqiqa)

> Prezentatsiya: **10–13-slaydlar**

### Aytiladigan gap

"Bugun bot yozamiz. Lekin avval bir narsani ko'rsataman."

Brauzerni oching va shu manzilni yozing (token o'rniga o'zingiznikini):

```
https://api.telegram.org/bot<TOKEN>/getMe
```

Ekranda JSON chiqadi:

```json
{"ok":true,"result":{"id":8377314125,"is_bot":true,"username":"u16_mashkabot"}}
```

**Shu paytda ayting:**

> "Ko'rdingizmi? Bu oddiy veb-manzil. Bot — bu Telegram serveriga HTTP so'rov yuboradigan dastur, boshqa hech nima. Biz yozadigan kutubxona — `aiogram` — shu so'rovlarni Python funksiyalariga aylantirib beradi. Ostida baribir shu."

### Doskaga chizing

```
   SIZ                          TELEGRAM
    │                               │
    │──── sendMessage ─────────────▶│   ← METOD (biz so'raymiz)
    │                               │
    │◀──── Update ──────────────────│   ← UPDATE (bizga keladi)
```

Ikki yo'nalish bor. Metodlar — biz yuboramiz. Update — bizga keladi.

### Savol bering

> "Telegram bizga qanday xabar beradi — biz so'raymizmi yoki u o'zi yuboradimi?"

Javob: ikkalasi ham mumkin. **Long polling** — bot o'zi so'rab turadi. **Webhook** — Telegram o'zi yuboradi. Biz polling bilan boshlaymiz, chunki domen va SSL kerak emas.

---

## 2-qism. Tayyorgarlik (15 daqiqa)

### Qadam 1 — Har bir o'quvchi o'z botini oladi

Telegramda **@BotFather** ni oching.

| Yozasiz | BotFather nima deydi |
|---|---|
| `/newbot` | "Alright, a new bot. How are we going to call it?" |
| `Mening birinchi botim` | "Good. Now let's choose a username" |
| `talaba_ali_bot` | Token beradi |

> **Diqqat.** Username `bot` bilan tugashi **shart** va butun Telegramda **yagona** bo'lishi kerak. Band bo'lsa, oxiriga raqam qo'shing: `talaba_ali_2026_bot`.

**Muhim qoida — o'quvchilarga ayting:**

> "Bitta token bilan bir vaqtda faqat bitta bot ishlaydi. Agar ikkovingiz bir xil tokendan foydalansangiz, ikkalangizda ham xato chiqadi. Shuning uchun har biringiz o'z botingizni yarating."

### Qadam 2 — Papka va virtual muhit

```bash
mkdir mening_botim
cd mening_botim
python3 -m venv .venv
source .venv/bin/activate
```

Windows'da oxirgi qator: `.venv\Scripts\activate`

**Nima uchun `venv` kerak** — shunday tushuntiring:

> "Tasavvur qiling, birinchi loyihangizga aiogram 3.30 kerak, ikkinchisiga 2.25. Global Python'ga o'rnatsangiz, ikkinchisi birinchisini buzadi. `venv` — har bir loyiha uchun alohida quti. Ichidagi paketlar tashqariga chiqmaydi."

Terminalda `(.venv)` yozuvi paydo bo'lganini ko'rsating — muhit faollashgani shu.

### Qadam 3 — Paketlarni o'rnatish

```bash
pip install aiogram python-dotenv
```

Tekshirish:

```bash
python -c "import aiogram; print(aiogram.__version__)"
```

`3.30.0` yoki undan yuqori chiqishi kerak.

> **Ogohlantiring:** "Internetda aiogram 2 bo'yicha juda ko'p eski dars bor. Agar kodda `@dp.message_handler` yoki `executor.start_polling` ko'rsangiz — bu eski versiya, bizga to'g'ri kelmaydi. Yopib qo'ying."

### Qadam 4 — Uchta fayl yarating

```bash
touch main.py .env .gitignore
```

**`.env`** — ichiga tokenni yozing:

```
BOT_TOKEN=8377314125:AAHxkX2xL4SewhBbIZACTzrE2De0vzK7UDQ
```

**`.gitignore`** — ichiga:

```
.venv/
__pycache__/
.env
```

**Nima uchun `.env` kerak** — bu joyda to'xtang va jiddiy ayting:

> "Token — bu parol. U bilan kim bo'lsa ham sizning botingizni to'liq boshqara oladi: xabar yuborishi, foydalanuvchilar bilan yozishishi mumkin. Shuning uchun uni hech qachon kod ichiga yozmaymiz va hech qachon GitHub'ga qo'ymaymiz. Agar tushib ketsa — BotFather'da `/revoke` qilasiz, eski token darhol o'ladi."

---

## 3-qism. Kod yozish (35 daqiqa)

Endi `main.py` ni **to'rt bosqichda** yozamiz. Har bosqichdan keyin **ishga tushiramiz** — o'quvchi natijani ko'rsin.

### 1-bosqich — Bot ishga tushsin (jim bo'lsa ham)

`main.py` ga yozing:

```python
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

dp = Dispatcher()


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
```

**Ishga tushiring:**

```bash
python main.py
```

Ekranda:

```
2026-08-20 18:26:30 | INFO | Bot ishga tushdi: @talaba_ali_bot
2026-08-20 18:26:30 | INFO | Start polling
```

**Botga Telegramda yozing** — javob bermaydi. Bu **to'g'ri**. Hali bironta handler yozmadik.

**To'xtatish:** `Ctrl + C`

### Har bir qatorni tushuntiring

| Qator | Nima qiladi |
|---|---|
| `load_dotenv()` | `.env` faylini o'qiydi, ichidagilarni `os.getenv` uchun tayyorlaydi |
| `logging.basicConfig(...)` | Ekranga chiroyli log chiqaradi. Xatolarni ko'rish uchun |
| `dp = Dispatcher()` | **Kiruvchi** yo'nalish. Update'ni olib, kerakli funksiyaga uzatadi |
| `Bot(token=...)` | **Chiquvchi** yo'nalish. Telegram'ga so'rov yuboradi |
| `DefaultBotProperties(parse_mode=HTML)` | Har xabarda `parse_mode="HTML"` yozmaslik uchun. Bir marta sozlaymiz |
| `await bot.get_me()` | Telegram'dan "men kimman?" deb so'raydi. Token to'g'riligini tekshiradi |
| `dp.start_polling(bot)` | Cheksiz sikl: so'ra → oling → uzating. Ctrl+C bosilguncha |
| `asyncio.run(main())` | Asinxron funksiyani ishga tushiradi |

### `async` nima uchun kerak — shunday tushuntiring

> "Tasavvur qiling, botga bir vaqtda 100 kishi yozdi. Oddiy dasturda bot birinchisiga javob berib bo'lguncha qolgan 99 tasi kutadi. `async` da esa bot birinchi so'rovni yuborib, javob kutayotganda ikkinchisini boshlaydi. Shuning uchun barcha handler'lar `async def` bo'ladi va ichida `await` ishlatiladi."

### 2-bosqich — `/start` ga javob

`dp = Dispatcher()` dan **keyin**, `async def main()` dan **oldin** qo'shing:

```python
from aiogram.filters import CommandStart
from aiogram.types import Message


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Salom, <b>{message.from_user.full_name}</b>!\n\n"
        f"Men birinchi botman. /help yozing."
    )
```

**Ishga tushiring, botga `/start` yozing.** Endi javob beradi.

**Tushuntiring:**

- `@dp.message(...)` — bu **dekorator**. "Bu funksiyani xabarlar uchun ro'yxatga ol" degani
- `CommandStart()` — **filtr**. "Faqat `/start` kelganda ishla"
- `message.answer(...)` — xabar kelgan chatga javob yuboradi
- `message.from_user.full_name` — yozgan odamning ismi
- `<b>...</b>` ishlayapti, chunki `parse_mode=HTML` ni oldindan sozlaganmiz

### 3-bosqich — `/help`

```python
from aiogram.filters import Command


@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "<b>Buyruqlar:</b>\n"
        "/start — boshlash\n"
        "/help — yordam\n\n"
        "Yoki oddiy matn yozing — men takrorlayman."
    )
```

Ishga tushiring, `/help` yozing.

### 4-bosqich — Echo (va eng muhim qoida)

```python
from aiogram import F


@dp.message(F.text)
async def echo(message: Message):
    await message.answer(f"Siz yozdingiz: {message.text}")
```

Ishga tushiring, `salom` deb yozing → `Siz yozdingiz: salom`.

---

## 4-qism. ATAYLAB XATO QILING (10 daqiqa)

> Bu darsning eng muhim 10 daqiqasi. O'tkazib yubormang.

### Xatoni ko'rsating

`echo` funksiyasini **`start` dan yuqoriga** ko'chiring. Ya'ni tartib shunday bo'lsin:

```python
@dp.message(F.text)          # ← endi birinchi
async def echo(message: Message):
    ...

@dp.message(CommandStart())  # ← endi ikkinchi
async def start(message: Message):
    ...
```

Ishga tushiring va `/start` yozing.

**Natija:** `Siz yozdingiz: /start`

`/start` handler'i **umuman ishlamadi**.

### Endi so'rang

> "Nima uchun shunday bo'ldi?"

O'quvchilar o'ylab ko'rsin. Keyin javobni ayting:

> **Aiogram update'ni yuqoridan pastga tekshiradi va birinchi mos kelgan handler'da to'xtaydi.** `F.text` — "har qanday matn" degani. `/start` ham matn. Shuning uchun echo uni birinchi bo'lib ushlab oldi va pastga o'tkazmadi.

**Doskaga yozing va rangli qalam bilan aylantiring:**

```
FILTRSIZ HANDLER — DOIM ENG OXIRIDA
```

Kodni qaytadan to'g'rilang va yana ishga tushiring — `/start` yana ishlaydi.

**Shu gapni qo'shing:**

> "Botdagi 'sababsiz ishlamayapti' muammolarining yarmi shu. Kelasi darslarda ham shu qoidaga qaytamiz."

---

## Dars natijasi

O'quvchida **ishlaydigan bot** bor:

| Yozadi | Bot javobi |
|---|---|
| `/start` | Salom, Ali Valiyev! |
| `/help` | Buyruqlar ro'yxati |
| `salom` | Siz yozdingiz: salom |

Tayyor kod: `darslar/1-dars/main.py`

---

## Uy vazifasi

1. Botga `/about` buyrug'ini qo'shing — o'zingiz haqingizda 2–3 qator yozsin
2. `/vaqt` buyrug'ini qo'shing — hozirgi vaqtni ko'rsatsin
   (maslahat: `from datetime import datetime`, keyin `datetime.now().strftime("%H:%M")`)
3. Echo handler'ini shunday o'zgartiring: agar xabar 100 belgidan uzun bo'lsa,
   "Juda uzun yozdingiz!" desin
4. **O'qish:** `BOT_YOZISH_QOLLANMA.md` — 1-dan 4-gacha bo'limlar

---

## Tez-tez chiqadigan xatolar

| Xato | Sabab | Yechim |
|---|---|---|
| `TelegramUnauthorizedError: Unauthorized` | Token noto'g'ri | `.env` ni tekshiring, ortiqcha bo'sh joy yoki qo'shtirnoq bo'lmasin |
| `ModuleNotFoundError: No module named 'aiogram'` | `venv` faollashmagan | `source .venv/bin/activate` |
| `TelegramConflictError` | Ikkita bot bir tokenda ishlayapti | Eskisini `Ctrl+C` bilan to'xtating |
| Bot javob bermayapti | Handler `main()` dan keyin yozilgan | Handler'lar `main()` dan **oldin** turishi kerak |
| `TypeError: 'NoneType' object` | `.env` topilmadi | `load_dotenv()` chaqirilganmi, `.env` shu papkadami |
