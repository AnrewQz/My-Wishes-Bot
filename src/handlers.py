from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram import html
from sqlite import create_wish, delete_wish, look_wishes, rent_wish, stop_rent
from keyboards import kb

router = Router()


class NewWishForm(StatesGroup):
    name = State()
    description = State()


class DeleteWishForm(StatesGroup):
    wish = State()


class LookWishesForm(StatesGroup):
    user = State()


class RentWishForm(StatesGroup):
    wish = State()


class StopRentWishForm(StatesGroup):
    wish = State()


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        f"Привет! Я бот, с помощью которого можно записывать свои хотелки, "
        f"давать им описание, чтобы другие пользователи увидели их и подарили Вам.\n\n"
        f"Вы тоже можете исполнять хотелки других.\n"
        f"Для этого их надо сначала забронировать, чтобы кто-то другой не подарил то же, что и вы.\n\n"
        f"Чтобы разобраться с кнопками, нажмите /help",
        reply_markup=kb
    )


@router.message(Command("help"))
async def command_help_handler(message: types.Message):
    await message.answer(
        f"/my_wishes - Посмотреть свои хотелки\n"
        f"/look_wishes - Посмотреть хотелки другого\n"
        f"/new_wish - Добавить новую хотелку\n"
        f"/delete_wish - Удалить хотелку\n"
        f"/rent_wish - Забронировать хотелку другого пользователя\n"
        f"/stop_rent_wish - Перестать бронировать чью-то хотлеку\n",
        reply_markup=kb
    )


@router.message(Command("my_wishes"))
async def command_my_wishes_handler(message: types.Message):
    result = await look_wishes("@" + message.from_user.username, check_myself=True)
    await message.answer(result, parse_mode=ParseMode.HTML, reply_markup=kb)


@router.message(Command("look_wishes"))
async def command_look_wishes_handler(message: types.Message, state: FSMContext):
    await state.set_state(LookWishesForm.user)
    await message.answer(f"Введите имя пользователя (в формате @user), чьи хотелки хотите посомтреть")


@router.message(LookWishesForm.user)
async def get_id_to_look_handler(message: types.Message, state: FSMContext):
    result = await look_wishes(message.text, check_myself=(message.text == "@" + message.from_user.username))
    await state.clear()
    await message.answer(result, parse_mode=ParseMode.HTML, reply_markup=kb)


@router.message(Command("new_wish"))
async def command_new_wish_handler(message: types.Message, state: FSMContext):
    await state.set_state(NewWishForm.name)
    await message.answer(f"Введите краткое название хотелки (одно предложение)")


@router.message(NewWishForm.name)
async def process_name_of_wish(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewWishForm.description)
    await message.answer(f"Можете написать подробное описание хотелки. "
                         f"Укажите все свои пожелания и всё, что может помочь тому, кто захочет Вам это поажрить:"
                         f"примерная цена, где это можно купить и т.д")


@router.message(NewWishForm.description)
async def process_description_of_wish(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    new_wish = await state.update_data(description=message.text)
    await state.clear()
    await create_wish(hash(new_wish.values), "@" + message.from_user.username, new_wish['name'],
                      new_wish['description'], "no_one")
    await message.answer(
        f"{html.bold('Ваша хотелка')}:\n"
        f"{new_wish['name']}\n"
        f"{html.bold('Описание')}:\n"
        f"{new_wish['description']}",
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )


@router.message(Command("delete_wish"))
async def command_delete_wish_handler(message: types.Message, state: FSMContext):
    await state.set_state(DeleteWishForm.wish)
    await message.answer(f"Введите id хотелки, которую хотите удалить")


@router.message(DeleteWishForm.wish)
async def command_delete_wish_handler(message: types.Message, state: FSMContext):
    result = await delete_wish(message.text, "@" + message.from_user.username)
    await state.clear()
    await message.answer(result, reply_markup=kb)


@router.message(Command("rent_wish"))
async def command_rent_wish_handler(message: types.Message, state: FSMContext):
    await state.set_state(RentWishForm.wish)
    await message.answer(f"Введите id хотелки, которую хотите забронировать")


@router.message(RentWishForm.wish)
async def command_rent_wish_handler(message: types.Message, state: FSMContext):
    result = await rent_wish(message.text, "@" + message.from_user.username)
    await state.clear()
    await message.answer(result, reply_markup=kb)


@router.message(Command("stop_rent_wish"))
async def command_stop_rent_handler(message: types.Message, state: FSMContext):
    await state.set_state(StopRentWishForm.wish)
    await message.answer(f"Введите id хотелки, которую хотите перестать бронировать")


@router.message(StopRentWishForm.wish)
async def command_stop_rent_handler(message: types.Message, state: FSMContext):
    result = await stop_rent(message.text, "@" + message.from_user.username)
    await state.clear()
    await message.answer(result, reply_markup=kb)


@router.message()
async def text_message_handler(message: types.Message):
    await message.answer("Я не умею отвечать на обычные сообщения. Используйте кнопки снизу", reply_markup=kb)
