import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType
from loguru import logger

from config_data.loader_bot import bot
from handlers import user_handlers, complain_handlers, assess_quality_repair

from aiogram import types, Dispatcher

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from states.tgbot_states import BaseStates, Complain, AssessQualityRepair


async def main(bot):
    logger.info('Start bot')
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LifetimeControllerMiddleware())

    dp.register_message_handler(user_handlers.start, commands=["start"], state="*")
    dp.register_message_handler(user_handlers.process_name, state=BaseStates.name)
    dp.register_callback_query_handler(user_handlers.ask_for_hand_contact, text='hand', state=BaseStates.phone)
    dp.register_callback_query_handler(
        user_handlers.ask_for_auto_contact, text='auto', state=BaseStates.phone)
    dp.register_message_handler(user_handlers.save_phone_contact,
                                content_types=[types.ContentType.CONTACT, types.ContentType.TEXT],
                                state=BaseStates.get_phone)
    dp.register_callback_query_handler(user_handlers.choose_options, text='send', state=BaseStates.choose_options)
    dp.register_callback_query_handler(user_handlers.get_choice, text=['complain', 'repair', 'idea'], state='*')

    dp.register_message_handler(complain_handlers.get_geolocation, state=Complain.get_geolocation)
    dp.register_callback_query_handler(complain_handlers.allowed_not_allowed, text=['allowed', 'not_allowed'],
                                       state=Complain.allowed_geolocation)
    dp.register_message_handler(complain_handlers.search_object, content_types=[ContentType.LOCATION],
                                state=Complain.search_object)
    dp.register_callback_query_handler(complain_handlers.select_from_list, state=Complain.select_from_list)
    dp.register_callback_query_handler(complain_handlers.check_exists_data_base, text='check', state=Complain.check_object_in_data_base)
    dp.register_callback_query_handler(complain_handlers.continue_or_stop, text=['continue', 'stop'],
                                       state=Complain.continue_or_stop)
    dp.register_callback_query_handler(complain_handlers.final_yes_no, text=['yes_back_to_start', 'no'], state=Complain.final_yes_no)
    dp.register_message_handler(complain_handlers.describe_problem, state=Complain.describe_problem)
    dp.register_message_handler(complain_handlers.photo_problem, content_types=[types.ContentType.PHOTO], state=Complain.photo_problem)

    dp.register_callback_query_handler(assess_quality_repair.leave_comment, state=AssessQualityRepair.leave_comment)
    dp.register_message_handler(assess_quality_repair.final_handler, state=AssessQualityRepair.final_handler)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main(bot))
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot Stopped')
