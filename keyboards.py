from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

button_register = KeyboardButton(text="Registration in tg-bot")
button_exchange_rates = KeyboardButton(text="Exchange rates")
button_tips = KeyboardButton(text="Economic advice")
button_finances = KeyboardButton(text="Personal finance")

fa_keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_register, button_exchange_rates],
    [button_tips, button_finances]
    ], resize_keyboard=True)

