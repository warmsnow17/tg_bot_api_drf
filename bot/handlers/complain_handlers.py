
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext


import keyboards.keyboards as kb
from lexicon.lexicon_ru import ALLOWED, SEND_GEOLOCATION, SELECT_FROM_LIST, YOUR_OBJECT_IS, OBJECT_IN_BASE
from states.tgbot_states import Complain


async def get_geolocation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(ALLOWED, reply_markup=kb.allowed_not_allowed())
    await state.set_state(Complain.allowed_geolocation)


async def allowed_not_allowed(callback_query: CallbackQuery, state: FSMContext):
    choice = callback_query.data
    if choice == 'allowed':
        await callback_query.message.answer(SEND_GEOLOCATION, reply_markup=kb.get_geolocation())
        await state.set_state(Complain.search_object)
    if choice == 'not_allowed':
        await callback_query.message.answer(SELECT_FROM_LIST, reply_markup=kb.select_from_list())
        await state.set_state(Complain.not_allowed_geolocation)
        await state.set_state(Complain.select_from_list)


async def search_object(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await state.update_data(location=location, latitude=latitude, longitude=longitude)
    await message.answer(f"Ваше местоположение: широта {latitude}, долгота {longitude}", reply_markup=kb.send_button())
    await state.set_state(Complain.select_from_list)


async def select_from_list(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    await state.update_data(_object=data)
    await callback_query.message.answer(YOUR_OBJECT_IS.format(_object=data), reply_markup=kb.check_exists_data_base())
    await state.set_state(Complain.check_object_in_data_base)


async def check_exists_data_base(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data("_object")
    my_data = data["_object"]
    if my_data == 'object1':
        await callback_query.message.answer(OBJECT_IN_BASE, reply_markup=kb.continue_or_stop())
        await state.set_state(Complain.continue_or_stop)
    if my_data == 'object2':
        await callback_query.message.answer("final")
        await state.finish()
    if my_data == 'send':
        await callback_query.message.answer("final22")
        await state.finish()

