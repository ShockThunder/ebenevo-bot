import telebot
import time
import os

token = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    # Проверяем, является ли пользователь администратором
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
    
    if chat_member.status not in ['administrator', 'creator']:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return
    
    if message.reply_to_message:
        # Если команда используется в реплае на сообщение
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username

        try:
            # Проверяем, является ли пользователь ботом
            user_info = bot.get_chat_member(message.chat.id, user_id)
            if user_info.user.is_bot:
                bot.reply_to(message, "Нельзя кикнуть другого бота.")
                return
            
            # Кикаем пользователя
            bot.kick_chat_member(message.chat.id, user_id)
            
            # Отправляем сообщение с ником и локальным изображением
            with open('./images/kick.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был кикнут.")
                
        except Exception as e:
            bot.reply_to(message, f"Не удалось кикнуть пользователя: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, которого хотите кикнуть.")



@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замутить администратора.")
        else:
            duration = 60 # Значение по умолчанию - 1 минута
            args = message.text.split()[1:]
            if args:
                try:
                    duration = int(args[0])
                except ValueError:
                    bot.reply_to(message, "Неправильный формат времени.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Максимальное время - 1 день.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            bot.reply_to(message, f"Пользователь {message.reply_to_message.from_user.username} замучен на {duration} минут.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замутить.")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        # Приветствуем нового участника
        bot.send_message(message.chat.id, f"Добро пожаловать, {new_member.first_name}! 🎉")

@bot.message_handler(content_types=['left_chat_member'])
def farewell_member(message):
    left_member = message.left_chat_member
    # Прощаемся с ушедшим участником
    bot.send_message(message.chat.id, f"Прощай, {left_member.first_name}! Мы будем по тебе скучать! 😢")

bot.infinity_polling(none_stop=True)