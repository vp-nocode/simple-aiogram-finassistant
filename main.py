import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import  Command
from aiogram.types import Message
from aiogram.fsm. context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm. storage. memory import MemoryStorage
import requests
import random

from config import TOKEN
from keyboards import fa_keyboard
from database import SessionLocal, User, user_exists, update_user_expenses
import logging

class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO)

@dp.message(Command('start'))
async def send_start(message: Message):
   await message.answer("Hello! I am your personal financial assistant. "
                        "Choose one of the options in the menu:", reply_markup=fa_keyboard)


@dp.message(F.text == "Registration in tg-bot")
async def registration(message: Message):
    telegram_id = message.from_user.id
    user_name = message.from_user.full_name
    session = SessionLocal()
    tb_user_exists = user_exists(session, telegram_id, user_name)
    if tb_user_exists:
        session.close()
        await message.reply("You are already registered!")
    else:
        tg_user = User(name=user_name, telegram_id=telegram_id)
        session.add(tg_user)
        session.commit()
        session.close()
        await message.reply("You have successfully registered!")


@dp.message(F.text == "Exchange rates")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/ac14eb420cdfc482c24676c8/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Unable to get exchange rates!")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']

        euro_to_rub = eur_to_usd * usd_to_rub

        await message.answer(f"1 USD - {usd_to_rub:.2f}  RUB\n"
                             f"1 EUR - {euro_to_rub:.2f}  RUB")

    except:
        await message.answer("An error occurred")


@dp.message(F.text == "Economic advice")
async def send_tips(message: Message):
    tips = [
       "Tip 1: Keep a budget and control your expenses.",
       "Tip 2: Put some of your expenses aside for savings.",
       "Tip 3: Buy products at discounts and sales."
    ]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == "Personal finance")
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Enter the first category of expenses:")

@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.reply("Enter expenses for category 1:")

@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1 = float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.reply("Enter the second category of expenses:")

@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2 = message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply("Enter expenses for category 2:")

@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2 = float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.reply("Enter the third category of expenses:")

@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3 = message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply("Enter expenses for category 3:")

@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses3=float(message.text))
    data = await state.get_data()
    telegram_id = message.from_user.id
    session = SessionLocal()
    update_user_expenses(session, telegram_id, new_category1=data['category1'],
                         new_category2=data['category2'], new_category3=data['category3'],
                         new_expenses1=data['expenses1'], new_expenses2=data['expenses2'],
                         new_expenses3=data['expenses3'])
    session.commit()
    session.close()
    await message.answer("Category and expenses saved!")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
