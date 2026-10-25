# ============================================================
#  Router'lar SHU YERDA ulanadi. TARTIB — eng muhim narsa.
#  Bu — Django'dagi urls.py ning ekvivalenti.
#
#  QOIDA: tordan kengga.
#    Aniq filtrli router'lar — yuqorida.
#    "Hamma narsani ushlaydigan" router — ENG OXIRIDA.
#
#  common.py ichida @router.message(F.text) bor — u HAR QANDAY
#  matnni ushlaydi. Agar common birinchi ulansa, u «🧺 Savat»
#  tugmasini ham yutib yuboradi va savat hech qachon ochilmaydi.
#
#  SINAB KO'RING: common.router ni yuqoriga ko'chiring va
#  «🧺 Savat» tugmasini bosing. Ishlamaydi. Keyin qaytaring.
# ============================================================

from aiogram import Dispatcher

from handlers import cart, catalog, common


def register(dp: Dispatcher) -> None:
    dp.include_router(cart.router)      # aniq: «🧺 Savat» va savat callback'lari
    dp.include_router(catalog.router)   # aniq: katalog callback'lari
    dp.include_router(common.router)    # /start + FALLBACK — eng oxirida
