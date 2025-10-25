import string
import random
from time import time

from core import ebenevobot
from modules import db_handler
from modules import adm_commands
from datetime import datetime

check_whitelist = adm_commands.check_whitelist

bot = ebenevobot.bot
who_game_db = db_handler.who_game_db
saved_messages_db = db_handler.saved_messages_db
query = db_handler.query

party_mode = True

keywords = {
    "да": "пизда",
    "нет": "пидора ответ",
    "молодец": "соси конец",
    "пизда": "да",
    "пидора ответ": "нет",
}

def clean_message(message):
    # Убираем знаки препинания
    message = message.translate(str.maketrans('', '', string.punctuation))
    # Убираем лишние слова
    words_to_remove = ["чат", "я", "и"]
    for word in words_to_remove:
        message = message.replace(word, "")
    # Убираем лишние пробелы
    message = ' '.join(message.split())
    return message

@bot.message_handler(commands=['explain_whogame'])
def explain_who_game(message):
    explanation = """На сообщение "кто" или "мы" я тегаю случайного человека из чата, как бы отвечая на вопрос. Такой прикол)\n\nЕсли не хочешь чтобы тебя тегали - нажми /noparty"""
    bot.reply_to(message, explanation)

@bot.message_handler(commands=['party'])
def add_user_to_party(message):
    check_whitelist(message)

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ''  # last_name может быть None

    # Проверка, существует ли пользователь в базе данных
    if not who_game_db.contains(query.user_id == user_id):
        # Если пользователь не существует, добавляем его в базу данных
        who_game_db.insert({'user_id': user_id, 'username': username, 'first_name': first_name, 'last_name': last_name})
        bot.reply_to(message, f"вас будут тегать")
    else:
        bot.reply_to(message, f"уже в списке")

@bot.message_handler(commands=['noparty'])
def add_user_to_party(message):
    check_whitelist(message)

    user_id = message.from_user.id

    if who_game_db.contains(query.user_id == user_id):
        who_game_db.remove(query.user_id == user_id)
        bot.reply_to(message, f"вас не будут тегать")
    else:
        bot.reply_to(message, f"тебя и так не трогали")

@bot.message_handler(commands=['partyoff'])
def party_off(message):
    check_whitelist(message)
    global party_mode
    party_mode = False
    bot.reply_to(message, f"Режим теганья выключен")    

@bot.message_handler(commands=['partyon'])
def party_on(message):
    check_whitelist(message)
    global party_mode
    party_mode = True
    bot.reply_to(message, f"Режим теганья включен")


def play_who_game(message, text):
    cleaned_message = clean_message(text.lower())
    if cleaned_message in ["кто", "мы"]:
        random_user= random.choice(who_game_db.all())
        if not random_user['username']:
            mention_link = f"tg://user?id={random_user['user_id']}"
            bot.reply_to(message, f"[{random_user['first_name']} {random_user['last_name']}]({mention_link})!"
                                  f"\nЧтобы выйти - /noparty"
                                  f"\nЧтобы играть - /party", parse_mode='Markdown') 
        else:
            bot.reply_to(message, f"@{random_user['username']}"
                                  f"\nЧтобы выйти - /noparty"
                                  f"\nЧтобы играть - /party") 

def save_message_link(message):
    # Получаем ссылку на сообщение и дату отправки
    chat_id = str(message.chat.id)[4:]
    message_link = f"https://t.me/c/{chat_id}/{message.message_id}"
    timestamp = int(time())  # <-- Сохраняем как число

    # Проверяем, существует ли запись для данного пользователя
    existing_user = saved_messages_db.get(query.user_id == message.from_user.id)
    user = message.from_user

    if existing_user:
        # Если запись существует, обновляем её
        saved_messages_db.update({'message_link': message_link, 'timestamp': timestamp}, query.user_id == user.id)
    else:
        # Если записи нет, создаем новую
        saved_messages_db.insert({'user_id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'message_link': message_link, 'timestamp': timestamp})

@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):  
    check_whitelist(message)      
    if not party_mode:
        return

    if not message.caption:
        return
    
    play_who_game(message, message.caption)

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):   
    check_whitelist(message)
    save_message_link(message)

    for keyword, response in keywords.items():
        if keyword == message.text.lower():
            if(keyword == "молодец" and message.from_user.id == 80207393):
                bot.reply_to(message, "спасибо")
            else:
                bot.reply_to(message, response)
            break  # Выходим из цикла после первого совпадения    

    if not party_mode:
            return

    play_who_game(message, message.text)