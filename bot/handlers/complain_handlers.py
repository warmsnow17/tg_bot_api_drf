
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from loguru import logger

import keyboards.keyboards as kb
from lexicon.lexicon_ru import ALLOWED, SEND_GEOLOCATION
from states.tgbot_states import Complain
from aiogram.types import ReplyKeyboardRemove


async def get_geolocation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(ALLOWED, reply_markup=kb.allowed_not_allowed())
    await state.set_state(Complain.allowed_geolocation)


async def allowed_geolocation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(SEND_GEOLOCATION, reply_markup=kb.get_geolocation())
    await state.set_state(Complain.search_object)


async def search_object(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await state.update_data(location=location, latitude=latitude, longitude=longitude)
    await message.answer(f"Ваше местоположение: широта {latitude}, долгота {longitude}", reply_markup=ReplyKeyboardRemove())
    await state.finish()
#подумать как данные из latitude longitude можно перевести в поиск по базы данных