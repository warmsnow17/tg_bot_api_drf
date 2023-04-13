from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

import keyboards.keyboards as kb
from bot import bot
from lexicon.lexicon_ru import ALLOWED, SEND_GEOLOCATION, SELECT_FROM_LIST, YOUR_OBJECT_IS, OBJECT_IN_BASE, THANK_YOU, \
    FINAL, CHOOSE_OPTIONS, DESCRIBE_PROBLEM, GET_PHOTO, THANKS_WE_WILL_CONTACT_YOU, DESCRIBE_PROBLEM_SECOND
from states.tgbot_states import Complain, BaseStates


async def get_geolocation(message: Message, state: FSMContext):
    await message.answer(ALLOWED, reply_markup=kb.allowed_not_allowed())
    await state.set_state(Complain.allowed_geolocation)


async def allowed_not_allowed(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
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
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = callback_query.data
    await state.update_data(_object=data)
    await callback_query.message.answer(YOUR_OBJECT_IS.format(_object=data), reply_markup=kb.check_exists_data_base())
    await state.set_state(Complain.check_object_in_data_base)


async def check_exists_data_base(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = await state.get_data("_object")
    my_data = data["_object"]
    if my_data == 'object1' or my_data == 'object2':
        await callback_query.message.answer(OBJECT_IN_BASE, reply_markup=kb.continue_or_stop())
        await state.set_state(Complain.continue_or_stop)
    if my_data == 'send':  # условие при котором объекта в базе данных нет
        await callback_query.message.answer(DESCRIBE_PROBLEM)
        await state.set_state(Complain.describe_problem)


async def continue_or_stop(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    choose_continue_or_stop = callback_query.data
    if choose_continue_or_stop == 'continue':
        await callback_query.message.answer(DESCRIBE_PROBLEM_SECOND)
        await state.set_state(Complain.describe_problem)
    if choose_continue_or_stop == 'stop':
        await callback_query.message.answer(THANK_YOU, reply_markup=kb.yes_no_kb())
        await state.set_state(Complain.final_yes_no)


async def describe_problem(message: Message, state: FSMContext):
    await state.update_data(describe_problem=message.text)
    await message.answer(GET_PHOTO)
    await state.set_state(Complain.photo_problem)


async def photo_problem(message: Message, state: FSMContext):
    await state.update_data(photo_problem=message.photo)
    await message.answer(THANKS_WE_WILL_CONTACT_YOU, reply_markup=kb.yes_no_kb())
    await state.set_state(Complain.final_yes_no)


async def final_yes_no(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    yes_no = callback_query.data
    if yes_no == 'yes_back_to_start':
        await callback_query.message.answer(CHOOSE_OPTIONS, reply_markup=kb.choose_options())
        await state.set_state(BaseStates.choose_options)

    if yes_no == 'no':
        await callback_query.message.answer(FINAL)
        await state.finish()
