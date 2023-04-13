from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    name = State()  # Состояние для получения имени пользователя
    phone = State()  # Состояние для получения номера телефона
    get_phone = State()
    choose_options = State()
    get_choice = State()


class Complain(BaseStates):
    get_geolocation = State()
    allowed_geolocation = State()
    search_object = State()
    select_from_list = State()
    not_allowed_geolocation = State()
    check_object_in_data_base = State()
    continue_or_stop = State()
    final_yes_no = State()
    describe_problem = State()
    photo_problem = State()
