from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
import keyboards.keyboards as kb
from config_data.loader_bot import bot
from handlers import complain_handlers
from handlers.complain_handlers import get_geolocation
from handlers.suggest_idea import describe_idea
from lexicon.lexicon_ru import SEND_AUTO_NUMBER, SEND_HAND_NUMBER, START_MESSAGE, CHOOSE_INPUT_TYPE, YOUR_PHONE_NUMBER, \
    CHOOSE_OPTIONS
from states.tgbot_states import BaseStates, Complain, SuggestIdea


# Хендлер для команды /start
async def start(message: Message, state: FSMContext):
    await message.answer(START_MESSAGE, reply_markup=types.ReplyKeyboardRemove())

    await state.set_state(BaseStates.name)


# Хендлер для получения имени пользователя
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(CHOOSE_INPUT_TYPE, reply_markup=kb.choose_phone_number())

    await state.set_state(BaseStates.phone)


# Хендлер для получения номера телефона, если выбран способ "Оставить автоматически"
async def ask_for_auto_contact(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(SEND_AUTO_NUMBER, reply_markup=kb.ask_for_contact())
    await state.set_state(BaseStates.get_phone)


async def ask_for_hand_contact(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    await callback_query.message.answer(SEND_HAND_NUMBER, reply_markup=ReplyKeyboardRemove())
    await state.set_state(BaseStates.get_phone)


async def save_phone_contact(message: Message, state: FSMContext):
    if message.content_type == types.ContentType.CONTACT:
        phone_number_auto_contact = message.contact.phone_number
        await state.update_data(phone_number=phone_number_auto_contact)
        await message.answer(
            YOUR_PHONE_NUMBER.format(phone_number=phone_number_auto_contact), reply_markup=kb.send_button())
    else:
        phone_number_text = message.text
        await state.update_data(phone_number=phone_number_text)
        await message.answer(YOUR_PHONE_NUMBER.format(phone_number=phone_number_text), reply_markup=kb.send_button())
    await state.set_state(BaseStates.choose_options)


async def choose_options(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await callback_query.message.answer(CHOOSE_OPTIONS, reply_markup=kb.choose_options())
    await state.set_state(BaseStates.get_choice)


async def get_choice(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await state.update_data(choose_options=callback_query.data)
    if callback_query.data == 'complain' or callback_query.data == 'repair':
        await state.set_state(Complain.get_geolocation)
        await get_geolocation(callback_query.message, state)
    if callback_query.data == 'idea':
        await state.set_state(SuggestIdea.describe_idea)
        await describe_idea(callback_query.message, state)







