from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

# confirmation_callback = CallbackData('confirmation', 'value')


def choose_phone_number():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button_manual = InlineKeyboardButton('Ввести в ручную', callback_data='hand')
    button_auto = InlineKeyboardButton('Оставить автоматически', callback_data='auto')
    keyboard.row(button_manual, button_auto)
    return keyboard


def ask_for_contact():
    # Создаем кнопку для запроса контакта
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Отправить номер телефона 📱", request_contact=True))
    return keyboard

