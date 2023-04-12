from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


# confirmation_callback = CallbackData('confirmation', 'value')


def choose_phone_number():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button_manual = InlineKeyboardButton('Ввести в ручную', callback_data='hand')
    button_auto = InlineKeyboardButton('Отправить автоматически', callback_data='auto')
    keyboard.row(button_manual, button_auto)
    return keyboard


def send_button():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    send_file_btn = InlineKeyboardButton('Отправить', callback_data='send_phone')
    keyboard.row(send_file_btn)
    return keyboard


def ask_for_contact():
    # Создаем кнопку для запроса контакта
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
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
