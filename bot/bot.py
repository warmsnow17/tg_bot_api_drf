from aiogram.utils import executor

from config_data.loader_bot import dp
from handlers import user_handlers, complain_handlers, assess_quality_repair, suggest_idea

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


dp.middleware.setup(LifetimeControllerMiddleware())

complain_handlers.register(dp=dp)
user_handlers.register(dp=dp)
assess_quality_repair.register(dp=dp)
suggest_idea.register(dp=dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

