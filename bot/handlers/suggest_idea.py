from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
import keyboards.keyboards as kb
from config_data.loader_bot import bot
from lexicon.lexicon_ru import DESCRIBE_IDEA, GET_PHOTO, THANKS_FOR_IDEA
from states.tgbot_states import SuggestIdea, Complain


async def describe_idea(message: Message, state: FSMContext):
    await message.answer(DESCRIBE_IDEA)
    await state.set_state(SuggestIdea.get_describe_idea)


async def get_describe_idea(message: Message, state: FSMContext):
    await state.update_data(describe_idea=message.text)
    await message.answer('Можете сделать фото', reply_markup=kb.send_foto_or_not())
    await state.set_state(SuggestIdea.send_foto_about_idea_or_not)


async def send_foto_about_idea_or_not(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if callback_query.data == 'send_photo':
        await callback_query.message.answer(GET_PHOTO)
        await state.set_state(SuggestIdea.send_foto)
    if callback_query.data == 'no_photo':
        await callback_query.message.answer(THANKS_FOR_IDEA, reply_markup=kb.yes_no_kb())
        await state.set_state(Complain.final_yes_no)


async def send_foto(message: Message, state: FSMContext):
    if message.photo is not None:
        await state.update_data(photo_idea=message.photo)
    await message.answer(THANKS_FOR_IDEA, reply_markup=kb.yes_no_kb())
    await state.set_state(Complain.final_yes_no)


def register(dp: Dispatcher):
    dp.register_message_handler(describe_idea, state=SuggestIdea.describe_idea)
    dp.register_message_handler(get_describe_idea,
                                state=SuggestIdea.get_describe_idea)
    dp.register_callback_query_handler(send_foto_about_idea_or_not,
                                       state=SuggestIdea.send_foto_about_idea_or_not)
    dp.register_message_handler(send_foto,
                                content_types=[ContentType.PHOTO],
                                state=SuggestIdea.send_foto)