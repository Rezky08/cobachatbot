import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot('1231725805:AAGNfddJG9WEEKhxgG5iSn6arrOq0m6qJ0c')
resource_url = 'https://cupbotresources.herokuapp.com/api'
accounts = []

def send_message_api_resources(content):
    return requests.post(url='{}/chat'.format(resource_url), data=content, headers={'Accept':'Application/json'})
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_chat = {
        'user_id' : message.from_user.id,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
        'text': message.text,
    }
    res = send_message_api_resources(user_chat)
    bot.send_message(message.chat.id,message.text,reply_to_message_id=message.message_id,reply_markup=types.ForceReply(selective=False))
bot.polling()