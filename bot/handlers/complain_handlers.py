from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.dispatcher import FSMContext
import base64, os
from loguru import logger
from api.interface import interface

import keyboards.keyboards as kb
from keyboards.callbackdata import road_callback, city_callback
from config_data.loader_bot import bot
from handlers.assess_quality_repair import quality_1_to_10
from lexicon.lexicon_ru import ALLOWED, SEND_GEOLOCATION, SELECT_FROM_LIST, YOUR_OBJECT_IS, OBJECT_IN_BASE, THANK_YOU, \
    FINAL, CHOOSE_OPTIONS, DESCRIBE_PROBLEM, GET_PHOTO, THANKS_WE_WILL_CONTACT_YOU, DESCRIBE_PROBLEM_SECOND
from states.tgbot_states import Complain, BaseStates, AssessQualityRepair


async def allowed_not_allowed(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    choice = callback_query.data
    if choice == 'allowed':
        await callback_query.message.answer(SEND_GEOLOCATION, reply_markup=kb.get_geolocation())
        await state.set_state(Complain.search_object)
    if choice == 'not_allowed':
        city_data = interface.get_cities_names()  # подумать правильная ли это запись можно ли if in json()?
        keyboard = kb.select_city(city_data)
        await callback_query.message.answer(SELECT_FROM_LIST, reply_markup=keyboard)
        # await state.set_state(Complain.not_allowed_geolocation)
        await state.set_state(Complain.select_from_list_pre)


async def select_from_list_pre(callback_query: CallbackQuery, callback_data: dict, state: FSMContext,):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    city_id = int(callback_data['id'])
    road_data = interface.get_roads(city_id)
    logger.warning(road_data)
    keyboard = kb.select_road(road_data)
    await callback_query.message.answer(text="Выберите улицу:", reply_markup=keyboard)
    await state.set_state(Complain.select_from_list)


async def search_object(message: Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await state.update_data(location=location, latitude=latitude, longitude=longitude)
    await message.answer(f"Ваше местоположение: широта {latitude}, долгота {longitude}", reply_markup=kb.send_button())
    await state.set_state(Complain.select_from_list)


async def select_from_list(callback_query: CallbackQuery, state: FSMContext, callback_data: dict):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(YOUR_OBJECT_IS.format(_object=callback_data['name']), reply_markup=kb.check_repair())
    await state.update_data(road=int(callback_data['id']))
    await state.set_state(Complain.check_object_in_data_base)


async def check_exists_data_base(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    data = await state.get_data()
    choose = callback_query.data
    if choose == 'check':
        if interface.check_status(data['road']):
            await callback_query.message.answer(OBJECT_IN_BASE,
                                          reply_markup=kb.continue_or_stop())
            await state.set_state(Complain.continue_or_stop)
        else:
            await callback_query.message.answer(DESCRIBE_PROBLEM)
            await state.set_state(Complain.describe_problem)
    else:
        pass # тут сделать кнопку назад


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
    await message.answer(THANKS_WE_WILL_CONTACT_YOU, reply_markup=kb.yes_no_kb())
    await state.set_state(Complain.final_yes_no)


async def final_yes_no(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    yes_no = callback_query.data
    if yes_no == 'yes_back_to_start':  # подумать как вноосим в state когда по второму разу юзер оставляет заявку
        await callback_query.message.answer(CHOOSE_OPTIONS, reply_markup=kb.choose_options())
        await state.finish()
        await state.set_state(BaseStates.choose_options)
    if yes_no == 'no':
        data = await state.get_data()
        if interface.send_report(data=data):
            await callback_query.message.answer(FINAL)
            logger.info('POST запрос ушел')
        else:
            await callback_query.message.answer('Произошла ошибка при отправке данных. Пожалуйста, попробуйте еще раз.')
            await state.finish()


# def road_page_callback(call):
#     page = int(call.data.split('#')[1])
#     bot.delete_message(
#         call.message.chat.id,
#         call.message.message_id
#     )
#     send_character_page(call.message, page)



def register(dp: Dispatcher):
    dp.register_callback_query_handler(select_from_list_pre,
                                       city_callback.filter(),
                                       state=Complain.select_from_list_pre)
    dp.register_callback_query_handler(allowed_not_allowed,
                                       text=['allowed', 'not_allowed'],
                                       state=Complain.allowed_geolocation)
    # dp.register_message_handler(search_object,
    #                             content_types=[ContentType.LOCATION],
    #                             state=Complain.search_object)
    # dp.register_callback_query_handler(road_page_callback,
    #                                    lambda call: call.data.split('#')[0] == 'road')
    dp.register_callback_query_handler(select_from_list,
                                       road_callback.filter(),
                                       state=Complain.select_from_list)
    dp.register_callback_query_handler(check_exists_data_base,
                                       text=['check', 'no_check'],
                                       state=Complain.check_object_in_data_base)
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