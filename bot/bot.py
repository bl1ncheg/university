import telebot
import requests
from telebot import types

API_TOKEN = '8130277578:AAEhS2T58Od9oqIjB9IiMw1RVOy_r33hjgI'
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения имен пользователей
usernames = {}

# Функция для получения курса доллара
def get_exchange_rate():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    return data['rates']['RUB']  # Верните курс доллара к рублю

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добрый день. Как вас зовут?")

@bot.message_handler(func=lambda message: message.chat.id not in usernames)
def get_name(message):
    chat_id = message.chat.id
    name = message.text

    # Сохраняем имя пользователя
    usernames[chat_id] = name
    
    rate = get_exchange_rate()
    send_rate_message(chat_id, name, rate)

@bot.message_handler(func=lambda message: message.chat.id in usernames)
def repeat_request_or_other(message):
    chat_id = message.chat.id
    name = usernames[chat_id]

    if message.text == "Запросить курс":
        rate = get_exchange_rate()
        bot.send_message(chat_id, f"Курс доллара сегодня {rate:.2f} р.", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Запросить курс"))
    else:
        bot.send_message(chat_id, f"Рад видеть вас снова, {name}! Вы можете запросить курс, нажав кнопку.")

def send_rate_message(chat_id, name, rate):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Запросить курс")
    markup.add(button)
    
    bot.send_message(chat_id, f"Рад знакомству, {name}! Курс доллара сегодня {rate:.2f} р.", reply_markup=markup)

bot.polling()
