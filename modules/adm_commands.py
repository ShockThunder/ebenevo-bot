import time

from core import ebenevobot
from data import db_handler

bot = ebenevobot.bot
admin_channel_id = ebenevobot.report_channel
db = db_handler.db
query = db_handler.query

def is_admin(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            return True
        else:
            return False

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/warn - выдать предупреждение\n/unwarn - снять предупреждение\n/mywarns - узнать количество своих варнов\n/checkwarns - узнать количество варнов пользователя\n/ban - забанить")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    # Проверяем, является ли пользователь администратором    
    if not is_admin(message):
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

                  #шлем сообщение в админский канал  
            bot.send_message(admin_channel_id, f"🔴 #КИК\n"
                                                f"• Кто: {message.reply_to_message.from_user.full_name} [{message.reply_to_message.from_user.id}]\n"
                                                f"• Группа: {message.chat.title} [{message.chat.id}]\n")

        except Exception as e:
            bot.reply_to(message, f"Не удалось кикнуть пользователя: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, которого хотите кикнуть.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    # Проверяем, является ли пользователь администратором    
    if not is_admin(message):
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
                bot.reply_to(message, "Нельзя банить другого бота.")
                return
            
            # Баним пользователя
            res = bot.ban_chat_member(message.chat.id, user_id)
            # Отправляем сообщение с ником и локальным изображением
            with open('./images/ban.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был забанен.")

            #шлем сообщение в админский канал
            bot.send_message(admin_channel_id, f"🔴 #БАН\n"
                                      f"• Кто: {message.reply_to_message.from_user.full_name} [{message.reply_to_message.from_user.id}]\n"
                                      f"• Группа: {message.chat.title} [{message.chat.id}]\n")

        except Exception as e:
            bot.reply_to(message, f"Не удалось забанить пользователя: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, которого хотите забанить.")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    # Проверяем, является ли пользователь администратором    
    if not is_admin(message):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return
    
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
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

@bot.message_handler(commands=['warn'])
def warn_user(message):
    # Проверяем, является ли пользователь администратором    
    if not is_admin(message):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return
    
    if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            user_data = db.get(query.id == user_id)
            if user_data:
                warnings_count = user_data['warnings'] + 1
                db.update({'warnings': warnings_count}, query.id == user_id)        
            else:
                db.insert({'id': user_id, 'warnings': 1})
                warnings_count = 1

            if warnings_count >= 3:
                bot.ban_chat_member(message.chat.id, user_id)
                            # Отправляем сообщение с ником и локальным изображением
                with open('./images/ban.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был кикнут за превышение количества предупреждений.")
                db.remove(query.id == user_id)
            else:
                with open('./images/warn.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} получил предупреждение. Всего предупреждений: {warnings_count}/3")

                #шлем сообщение в админский канал
                bot.send_message(admin_channel_id, f"⚠️ #ПРЕДУПРЕЖДЕНИЕ\n"
                                      f"• Кто: {message.reply_to_message.from_user.full_name} [{message.reply_to_message.from_user.id}]\n"
                                      f"• Группа: {message.chat.title} [{message.chat.id}]\n")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, которому хотите выдать предупреждение.")

@bot.message_handler(commands=['unwarn'])
def unwarn_user(message):
    # Проверяем, является ли пользователь администратором    
    if not is_admin(message):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_data = db.get(query.id == user_id)
        
        if user_data:
            warnings_count = user_data['warnings']
            if warnings_count > 0:
                warnings_count -= 1
                db.update({'warnings': warnings_count}, query.id == user_id)
                
                if warnings_count == 0:
                    # Если предупреждений больше нет, можно удалить пользователя из базы
                    db.remove(query.id == user_id)
                    with open('./images/unwarn.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{message.reply_to_message.from_user.username} больше не имеет предупреждений.")
                else:
                    with open('./images/light_unwarn.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{message.reply_to_message.from_user.username} теперь имеет {warnings_count} предупреждений.")
            else:
                bot.reply_to(message, f"У пользователя @{message.reply_to_message.from_user.username} нет предупреждений.")
        else:
            bot.reply_to(message, "Пользователь не имеет предупреждений.")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, у которого хотите снять предупреждение.")

@bot.message_handler(commands=['mywarns'])
def my_warns(message):
    user_id = message.from_user.id
    user_data = db.get(query.id == user_id)
    
    if user_data:
        warnings_count = user_data['warnings']
        bot.reply_to(message, f"У вас {warnings_count} предупреждений.")
    else:
        bot.reply_to(message, "У вас нет предупреждений.")

@bot.message_handler(commands=['checkwarns'])
def check_warns(message):
    # Проверяем, является ли пользователь администратором    
    if not is_admin(message):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return
    
    # Проверяем, указано ли сообщение с ID пользователя
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
    else:
        # Если команда не была вызвана в ответ на сообщение, покажем свои варны
        user_id = message.from_user.id
        username = message.from_user.username
        user_data = db.get(query.id == user_id)
    
    user_data = db.get(query.id == user_id)
    
    if user_data:
        warnings_count = user_data['warnings']
        bot.reply_to(message, f"Пользователь @{username} имеет {warnings_count} предупреждений.")
    else:
        bot.reply_to(message, f"У пользователя @{username} нет предупреждений.")