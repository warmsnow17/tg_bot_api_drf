from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
import keyboards.keyboards as kb
from config_data.loader_bot import bot
from lexicon.lexicon_ru import QUALITY_1_TO_10, YOUR_COMMENT, THANKS_FOR_QUALITY
from states.tgbot_states import AssessQualityRepair, Complain


async def quality_1_to_10(message: Message, state: FSMContext):
    await message.answer(QUALITY_1_TO_10, reply_markup=kb.quality_1_to_10())
    await state.set_state(AssessQualityRepair.leave_comment)


async def leave_comment(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await state.update_data(quality=callback_query.data)
    await callback_query.message.answer(YOUR_COMMENT)
    await state.set_state(AssessQualityRepair.final_handler)


async def final_handler(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer(THANKS_FOR_QUALITY, reply_markup=kb.yes_no_kb())
    await state.set_state(Complain.final_yes_no)
