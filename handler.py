import time
from datetime import timedelta

from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from state import BuyState
from keyboard import message_keyboard, buy_keyboard, conf_keyboard, site_keyboard, GetData, BuyData, ConfBuyData
from books import db, search_books
from sheets import append_line

router = Router()
init_ts = time.perf_counter()

requests = []

def uptime() -> int:
    return round(time.perf_counter() - init_ts)


@router.message(Command("ping"), StateFilter(None))
async def ping(message: types.Message):
    start = time.perf_counter_ns()
    message2 = await message.answer("🌒")

    await message2.edit_text(
        f"🏓 Ping: {round((time.perf_counter_ns() - start) / 10 ** 6, 3)} ms\n📡 Uptime: {str(timedelta(seconds=uptime()))}"
    )


@router.message(Command("start"), StateFilter(None))
async def start(message: types.Message):
    await message.answer(
        text="Привет! Я помогу тебе найти книгу по автору или названиию\nИли напиги комманду /site"
    )

@router.message(Command("site"), StateFilter(None))
async def site(message: types.Message):
    await message.answer("Нажмите на кнопку для открытия веб-приложения",
                         reply_markup=await site_keyboard())


@router.message(F.text, StateFilter(None))
async def answer_message(message: types.Message):
    msg = await message.answer("Ищу книги...")

    datas = await search_books(message.text)
    if datas is None:
        await msg.edit_text(text="Я ничего не нашел :(")
        return

    await msg.edit_text(
        text="Вот что я нашел",
        reply_markup=await message_keyboard(datas, db)
    )

@router.callback_query(F.data == "delete")
async def delete_message(call: types.CallbackQuery):
    await call.message.delete()

@router.callback_query(GetData.filter())
async def get_data(call: types.CallbackQuery, callback_data: GetData):
    data = db[callback_data.id]
    await call.message.answer(
        text=f"Название: {data['title']}\n"
             f"{'Автор' if len(data['authors']) == 1 else 'Авторы'}: {', '.join(data['authors'])}",
        reply_markup=await buy_keyboard(callback_data.id)
    )


@router.callback_query(BuyData.filter())
async def buy_callback(call: types.CallbackQuery, callback_data: BuyData, state: FSMContext):
    await call.message.answer(
        text="Скажите свое имя"
    )

    await state.update_data(id_=callback_data.id)
    await state.set_state(BuyState.name)

@router.message(BuyState.name)
async def buy_state_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(
        text="Скажите свой email"
    )

    await state.set_state(BuyState.email)


@router.message(BuyState.email)
async def buy_state_name(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)

    await message.answer(
        text="Скажите свой номер телефона"
    )

    await state.set_state(BuyState.phone)

@router.message(BuyState.phone)
async def buy_state_name(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await message.answer(
        text="Скажите свой адрес"
    )

    await state.set_state(BuyState.address)

@router.message(BuyState.address)
async def buy_state_name(message: types.Message, state: FSMContext):
    address = message.text

    data = await state.get_data()
    data["address"] = address

    book = db[data["id_"]]

    requests.append(data)

    await message.answer(
        text=f"Имя: {data['name']}\n"
             f"Почта: {data['email']}\n"
             f"Адрес: {address}\n"
             f"Номер телефона: {data['phone']}\n"
             f"Книга: {book['title']}\n"
              f"{'Автор' if len(book['authors']) == 1 else 'Авторы'}: {', '.join(book['authors'])}",
        reply_markup=await conf_keyboard(id=len(requests)-1)
    )

    await state.clear()


@router.callback_query(ConfBuyData.filter())
async def conf_callback(call: types.CallbackQuery, callback_data: ConfBuyData):
    data = requests[callback_data.id]
    book = db[data["id_"]]

    await append_line(
        [
            data['name'],
            data['email'],
            data['phone'],
            data['address'],
            book['title'],
            ', '.join(book['authors']),
        ]
    )

    await call.message.answer(
        text="Запрос на покупку отправлен, мы с вами свяжемся"
    )
