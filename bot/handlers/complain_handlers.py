import requests
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.dispatcher import FSMContext
import base64, os

from aiogram.utils.exceptions import MessageToDeleteNotFound
from loguru import logger

from api.get_location import get_location_details
from api.interface import interface

import keyboards.keyboards as kb
from handlers.user_handlers import get_choice
from keyboards.callbackdata import road_callback, city_callback
from config_data.loader_bot import bot, dp
from handlers.assess_quality_repair import quality_1_to_10
from lexicon.lexicon_ru import ALLOWED, SEND_GEOLOCATION, SELECT_FROM_LIST, YOUR_OBJECT_IS, OBJECT_IN_BASE, THANK_YOU, \
    FINAL, CHOOSE_OPTIONS, DESCRIBE_PROBLEM, GET_PHOTO, THANKS_WE_WILL_CONTACT_YOU, DESCRIBE_PROBLEM_SECOND, \
    OBJECT_NOT_IN_DB
from states.tgbot_states import Complain, BaseStates, AssessQualityRepair


async def allowed_not_allowed(callback_query: CallbackQuery, state: FSMContext, force_not_allowed=False):
    if force_not_allowed:
        choice = 'not_allowed'
    else:
        choice = callback_query.data
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except MessageToDeleteNotFound:
        pass
    if choice == 'allowed':
        try:
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        except MessageToDeleteNotFound:
            pass
        await callback_query.message.answer(SEND_GEOLOCATION, reply_markup=kb.get_geolocation())
        if await state.get_state() == 'Complain:allowed_geolocation':
            await state.set_state(Complain.search_object)
        else:
            await state.set_state(AssessQualityRepair.search_object)
    if choice == 'not_allowed':
        try:
            await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        except MessageToDeleteNotFound:
            pass
        city_data = interface.get_cities_names()
        keyboard = kb.select_city(city_data, current_page=1)
        await callback_query.message.answer(SELECT_FROM_LIST, reply_markup=keyboard)
        if await state.get_state() == 'Complain:allowed_geolocation':
            await state.set_state(Complain.select_from_list_pre)
        else:
            await state.set_state(AssessQualityRepair.select_from_list_pre)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('city_data_page_'), state='*')
async def change_city_page(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "ignore":
        await callback_query.answer()
        return

    callback_data = callback_query.data.split('_')
    current_page = int(callback_data[-1])
    items_per_page = 5
    state_data = await state.get_data()

    city_data = interface.get_cities_names()
    keyboard = kb.select_city(city_data, current_page)
    await callback_query.message.edit_text(text=SELECT_FROM_LIST, reply_markup=keyboard)


async def select_from_list_pre(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    logger.warning(await state.get_state())
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    city_id = int(callback_data['id'])
    road_data = interface.get_roads(city_id)
    logger.warning(road_data)
    keyboard = kb.select_road(road_data, current_page=1)
    await callback_query.message.answer(text="Выберите улицу:", reply_markup=keyboard)

    await state.update_data(city_id=city_id)

    if 'Complain' in await state.get_state():
        await state.set_state(Complain.select_from_list)
    else:
        await state.set_state(AssessQualityRepair.select_from_list)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('road_data_page_'), state='*')
async def change_page(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "ignore":
        await callback_query.answer()
        return

    callback_data = callback_query.data.split('_')
    current_page = int(callback_data[-1])
    items_per_page = 10
    state_data = await state.get_data()
    city_id = state_data['city_id']

    road_data = interface.get_roads(city_id)
    keyboard = kb.select_road(road_data, current_page)
    await callback_query.message.edit_text(text="Выберите улицу:", reply_markup=keyboard)


async def search_object(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude

    city, road_name = await get_location_details(latitude, longitude)
    road_id = interface.get_road_id_by_name(road_name)
    if road_id:
        await message.answer(
            f"Город: {city}\nУлица: {road_name}",
            reply_markup=kb.send_geo_button(road_name, road_id),
        )
        await state.update_data(road=road_id)
        if 'Complain' in await state.get_state():
            await state.set_state(Complain.select_from_list)
        else:
            await state.set_state(AssessQualityRepair.select_from_list)
    else:
        await message.answer(OBJECT_NOT_IN_DB.format(city=city, road_name=road_name))
        await message.answer(CHOOSE_OPTIONS, reply_markup=kb.choose_options())
        data = await state.get_data()
        username = data['username']
        phone = data['phone']
        await state.finish()
        await state.set_state(BaseStates.choose_options)
        await state.update_data(username=username)
        await state.update_data(phone=phone)


async def select_from_list(callback_query: CallbackQuery, state: FSMContext, callback_data: dict):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(YOUR_OBJECT_IS.format(_object=callback_data['name']), reply_markup=kb.check_repair())
    await state.update_data(road=int(callback_data['id']))
    if 'Complain' in await state.get_state():
        await state.set_state(Complain.check_object_in_data_base)
    else:
        await state.set_state(AssessQualityRepair.check_object_in_data_base)


async def check_exists_data_base(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = await state.get_data()
    print(data['road'])
    choose = callback_query.data
    if choose == 'check':
        if 'Complain' in await state.get_state():
            info = interface.check_status(data['road'])
            print(info)
            if info[0]:
                await callback_query.message.answer(OBJECT_IN_BASE.format(period=info[1]),
                                            reply_markup=kb.continue_or_stop())
                await state.set_state(Complain.continue_or_stop)
            else:
                await callback_query.message.answer(DESCRIBE_PROBLEM)
                await state.set_state(Complain.describe_problem)
        else:
            await quality_1_to_10(callback_query.message, state)
    elif choose == 'no_check':
        await allowed_not_allowed(callback_query, state, force_not_allowed=True)


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
    await state.update_data(text=message.text)
    await message.answer(GET_PHOTO)
    await state.set_state(Complain.photo_problem)


async def photo_problem(message: Message, state: FSMContext):
    photo = await message.photo[-1].download()
    with open(photo.name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    ext = photo.name.split('.')[-1]
    dataurl = f'data:image/{ext};base64,{encoded_string}'
    await state.update_data(photo=dataurl)
    os.remove(photo.name)
    data = await state.get_data()
    if interface.send_report(data, interface.reports_url):
        await message.answer(THANKS_WE_WILL_CONTACT_YOU, reply_markup=kb.yes_no_kb())
        await state.set_state(Complain.final_yes_no)
    else:
        await message.answer('Произошла ошибка при отправке данных. Пожалуйста, попробуйте еще раз.')
        await state.finish()


async def final_yes_no(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    yes_no = callback_query.data
    if yes_no == 'yes_back_to_start':  # подумать как вноосим в state когда по второму разу юзер оставляет заявку
        await callback_query.message.answer(CHOOSE_OPTIONS, reply_markup=kb.choose_options())
        data = await state.get_data()
        username = data['username']
        phone = data['phone']
        await state.finish()
        await state.set_state(BaseStates.choose_options)
        await state.update_data(username=username)
        await state.update_data(phone=phone)
    if yes_no == 'no':
        await callback_query.message.answer(FINAL)
        await state.finish()


def register(dp: Dispatcher):
    dp.register_callback_query_handler(select_from_list_pre,
                                       city_callback.filter(),
                                       state=[Complain.select_from_list_pre,
                                              AssessQualityRepair.select_from_list_pre])
    dp.register_callback_query_handler(select_from_list_pre,
                                       state=[Complain.select_from_list_pre,
                                              AssessQualityRepair.select_from_list_pre])
    dp.register_callback_query_handler(allowed_not_allowed,
                                       state=[Complain.allowed_geolocation,
                                              AssessQualityRepair.allowed_geolocation])
    dp.register_message_handler(search_object,
                                content_types=[ContentType.LOCATION],
                                state=Complain.search_object)
    dp.register_callback_query_handler(allowed_not_allowed,
                                       state=[Complain.allowed_geolocation,
                                              AssessQualityRepair.allowed_geolocation])
    dp.register_callback_query_handler(select_from_list,
                                       road_callback.filter(),
                                       state=[Complain.select_from_list,
                                              AssessQualityRepair.select_from_list])
    dp.register_callback_query_handler(check_exists_data_base,
                                       text=['check', 'no_check'],
                                       state=[Complain.check_object_in_data_base,
                                              AssessQualityRepair.check_object_in_data_base])
    dp.register_callback_query_handler(continue_or_stop,
                                       text=['continue', 'stop'],
                                       state=Complain.continue_or_stop)
    dp.register_callback_query_handler(final_yes_no,
                                       text=['yes_back_to_start', 'no'],
                                       state=Complain.final_yes_no)
    dp.register_message_handler(describe_problem,
                                state=Complain.describe_problem)
    dp.register_message_handler(photo_problem,
                                content_types=[ContentType.PHOTO],
                                state=Complain.photo_problem)