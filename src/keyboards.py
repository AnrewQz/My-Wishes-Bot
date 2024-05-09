from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

help_button = KeyboardButton(text="/help")
new_wish_button = KeyboardButton(text="/new_wish")
look_wishes_button = KeyboardButton(text="/look_wishes")
my_wishes_button = KeyboardButton(text="/my_wishes")
rent_wish_button = KeyboardButton(text="/rent_wish")
delete_wish_button = KeyboardButton(text="/delete_wish")
stop_rent_wish_button = KeyboardButton(text="/stop_rent_wish")

builder = ReplyKeyboardBuilder()

builder.add(help_button)
builder.row(my_wishes_button, look_wishes_button)
builder.row(new_wish_button, delete_wish_button)
builder.row(rent_wish_button, stop_rent_wish_button)

kb = builder.as_markup(resize_keyboard=True)
