import logging
import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

TOKEN = "8037349465:AAEf-bVkQsBl18vZmJI3gRh_iWe-ztqAYL4"
ADMIN_ID = 1324688385  # ID Натали

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Состояния для скидки и консультации
class DiscountForm(StatesGroup):
    name = State()
    phone = State()

class HealthForm(StatesGroup):
    name = State()
    phone = State()

# Команда /start
@router.message(F.text == "/start")
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💄 Красота и уход"), KeyboardButton(text="💊 Здоровье")],
            [KeyboardButton(text="🎁 Получить скидку")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Здравствуйте! Я помогу вам с выбором продукции и получением скидок.\n\nПожалуйста, выберите, что вас интересует:",
        reply_markup=keyboard
    )

# Команда /help
@router.message(F.text == "/help")
async def cmd_help(message: Message):
    await message.answer("""Вот что я умею:
/start – Начать общение
/help – Как пользоваться ботом
/discount – Получить скидку
/products – Посмотреть каталог
/contact – Связаться с Натальей""")

# Команда /products
@router.message(F.text == "/products")
async def cmd_products(message: Message):
    await message.answer("📦 Каталог продукции: https://meitanglobal.com/catalog/?ref=782833")

# Команда /contact
@router.message(F.text == "/contact")
async def cmd_contact(message: Message):
    await message.answer("📲 Связаться с Натальей: https://t.me/nataliaosipova8164")

# Кнопка «🎁 Получить скидку»
@router.message(F.text.in_({"🎁 Получить скидку", "/discount"}))
async def discount_start(message: Message, state: FSMContext):
    await state.set_state(DiscountForm.name)
    await message.answer("Как вас зовут?", reply_markup=ReplyKeyboardRemove())

@router.message(DiscountForm.name)
async def discount_get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(DiscountForm.phone)
    await message.answer("Укажите номер телефона:")

@router.message(DiscountForm.phone)
async def discount_get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    phone = message.text
    try:
        await bot.send_message(ADMIN_ID, f"🎁 Заявка на скидку:\nИмя: {name}\nТелефон: {phone}")
    except Exception as e:
        print(f"❌ Ошибка при отправке уведомления админу: {e}")
    await message.answer("Спасибо! Наталья свяжется с вами в ближайшее время 😊")
    await state.clear()

# Кнопка «Красота и уход»
@router.message(F.text == "💄 Красота и уход")
async def beauty_section(message: Message, state: FSMContext):
    await message.answer(
        "🌸 Популярные продукты:\n"
        "— Гель Dao de Mei\n"
        "— Крем NeoCollagen\n"
        "— Патчи с пептидами\n\n"
        "Если вас что-то заинтересовало — напишите, и Наталья подберёт лучшее решение."
    )
    await state.set_state(HealthForm.name)

# Кнопка «Здоровье»
@router.message(F.text == "💊 Здоровье")
async def health_section(message: Message, state: FSMContext):
    await message.answer(
        "🌿 Натуральные средства:\n"
        "✔️ Суставы\n✔️ Иммунитет\n✔️ ЖКТ\n✔️ Женское здоровье\n\n"
        "Напишите, что вас беспокоит — Наталья поможет подобрать средство."
    )
    await state.set_state(HealthForm.name)

@router.message(HealthForm.name)
async def get_health_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(HealthForm.phone)
    await message.answer("Пожалуйста, укажите номер телефона:")

@router.message(HealthForm.phone)
async def get_health_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    phone = message.text
    try:
        await bot.send_message(ADMIN_ID, f"💬 Заявка на консультацию по продукции:\nИнтересует: {name}\nТелефон: {phone}")
    except Exception as e:
        print(f"❌ Ошибка при отправке уведомления админу: {e}")
    await message.answer("Спасибо! Наталья свяжется с вами для консультации 😊")
    await state.clear()

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())