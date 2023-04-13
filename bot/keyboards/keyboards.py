from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# confirmation_callback = CallbackData('confirmation', 'value')


def choose_phone_number():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button_manual = InlineKeyboardButton('Ввести в ручную', callback_data='hand')
    button_auto = InlineKeyboardButton('Отправить автоматически', callback_data='auto')
    keyboard.row(button_manual)
    keyboard.row(button_auto)
    return keyboard


def send_button():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    send_file_btn = InlineKeyboardButton('Отправить', callback_data='send')
    keyboard.row(send_file_btn)
    return keyboard


def check_exists_data_base():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    send_file_btn = InlineKeyboardButton('Проверить есть ли в базе данных', callback_data='check')
    keyboard.row(send_file_btn)
    return keyboard


def ask_for_contact():
    # Создаем кнопку для запроса контакта
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
    return keyboard


def choose_options():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    complain_bad_road = InlineKeyboardButton("Пожаловаться на плохую дорогу", callback_data='complain')
    assess_quality_repair = InlineKeyboardButton("Оценить качество ремонта", callback_data='repair')
    suggest_idea = InlineKeyboardButton("Предложить идею", callback_data='idea')
    keyboard.row(complain_bad_road)
    keyboard.row(assess_quality_repair)
    keyboard.row(suggest_idea)
    return keyboard


def allowed_not_allowed():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    allowed = InlineKeyboardButton("Разрешить", callback_data='allowed')
    not_allowed = InlineKeyboardButton("Выбрать из списка объектов", callback_data='not_allowed')
    keyboard.row(allowed)
    keyboard.row(not_allowed)
    return keyboard


def get_geolocation():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Отправить местоположение 📍", request_location=True))
    return keyboard


def select_from_list():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    object_1 = InlineKeyboardButton("объект 1", callback_data='object1')
    object_2 = InlineKeyboardButton("объект 2", callback_data='object2')
    object_3 = InlineKeyboardButton("объект 3", callback_data='object')
    keyboard.row(object_1)
    keyboard.row(object_2)
    keyboard.row(object_3)
    return keyboard


def continue_or_stop():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    continue_ = InlineKeyboardButton("Продолжить", callback_data='continue')
    stop_ = InlineKeyboardButton("Дождемся ремонта", callback_data='stop')
    keyboard.row(continue_)
    keyboard.row(stop_)
    return keyboard


def yes_no_kb():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    yes = InlineKeyboardButton("Да", callback_data='yes_back_to_start')
    no = InlineKeyboardButton("Нет", callback_data='no')
    keyboard.row(yes)
    keyboard.row(no)
    return keyboard


def quality_1_to_10():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    for i in range(1, 11):
        button = InlineKeyboardButton(str(i), callback_data=str(i))
        keyboard.row(button)

    return keyboard

