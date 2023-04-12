from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    name = State()  # Состояние для получения имени пользователя
    phone = State()  # Состояние для получения номера телефона
    get_phone = State()
    choose_options = State()
    end = State()