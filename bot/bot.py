import asyncio
from loguru import logger

from handlers import user_handlers
from config_data.config import Config, load_config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from states.tgbot_states import BaseStates


async def main():
    logger.info('Start bot')
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

    dp.middleware.setup(LifetimeControllerMiddleware())

    dp.register_message_handler(user_handlers.start, commands=["start"], state="*")

    dp.register_message_handler(user_handlers.process_name, state=BaseStates.name)
    dp.register_callback_query_handler(user_handlers.ask_for_hand_contact, text='hand', state=BaseStates.phone)
    dp.register_callback_query_handler(
        user_handlers.ask_for_auto_contact, text='auto', state=BaseStates.phone)
    dp.register_message_handler(user_handlers.auto_phone_contact, content_types=types.ContentType.CONTACT,
                                state=BaseStates.get_auto_phone)
    dp.register_message_handler(user_handlers.hand_phone_contact, state=BaseStates.get_hand_phone)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot Stopped')
