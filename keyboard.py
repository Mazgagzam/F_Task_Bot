from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import WebAppInfo


class GetData(CallbackData, prefix="data"):
    id: int

class BuyData(CallbackData, prefix="buy"):
    id: int

class ConfBuyData(CallbackData, prefix="conf"):
    id: int


async def message_keyboard(datas, db):
    if datas is None:
        return None

    builder = InlineKeyboardBuilder()

    for data in datas:
        ind = db.index(data)

        builder.button(
            text=f"Название: {data['title']}",
            callback_data=GetData(id=ind)
        )
        builder.button(
            text="Купить",
            callback_data=GetData(id=ind)
        )

    builder.adjust(2)
    return builder.as_markup()

async def buy_keyboard(id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Купить",
        callback_data=BuyData(id=id)
    )

    builder.button(
        text="Назад",
        callback_data="delete"
    )

    return builder.as_markup()

async def conf_keyboard(id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Купить",
        callback_data=ConfBuyData(id=id)
    )

    return builder.as_markup()

async def site_keyboard():
    keyboard = InlineKeyboardBuilder()
    web_app = WebAppInfo(url="https://mazga.2d565027.nip.io/")  # URL вашего веб-приложения
    keyboard.button(text="Веб-приложение", web_app=web_app)


    return keyboard.as_markup()
