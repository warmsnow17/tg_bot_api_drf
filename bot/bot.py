import asyncio
from loguru import logger
from aiogram import Dispatcher, Bot
from config_data.config import load_config
from handlers import user_handlers


config = load_config()

bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher()

dp.include_router(user_handlers.router)


async def main():
    logger.info('Start bot')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
