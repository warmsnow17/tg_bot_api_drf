from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
import keyboards.stngs_kbd as kb
from lexicon.lexicon_ru import SEND_AUTO_NUMBER, SEND_HAND_NUMBER, START_MESSAGE, CHOOSE_INPUT_TYPE, YOUR_PHONE_NUMBER
from states.tgbot_states import BaseStates


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
    await callback_query.message.answer(SEND_AUTO_NUMBER, reply_markup=kb.ask_for_contact())
    await state.set_state(BaseStates.get_auto_phone)


async def auto_phone_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    if phone_number is not None:
        await state.update_data(phone_number=phone_number)
        await message.answer(YOUR_PHONE_NUMBER.format(phone_number=phone_number)) # тут написать что дальше по списку


# этот хендлер обрабатывает кнопка Ввести в ручную
async def ask_for_hand_contact(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(SEND_HAND_NUMBER,
                                        reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(BaseStates.get_hand_phone)


async def hand_phone_contact(message: Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await message.answer(YOUR_PHONE_NUMBER.format(phone_number=phone_number))
