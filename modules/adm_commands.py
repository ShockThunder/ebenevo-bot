from time import time

from core import ebenevobot
from modules import db_handler
from datetime import datetime, timedelta

bot = ebenevobot.bot
admin_channel_id = ebenevobot.report_channel
whitelist = ebenevobot.whitelist
db = db_handler.db
saved_messages_db = db_handler.saved_messages_db
who_game_db = db_handler.who_game_db
query = db_handler.query

def is_admin(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            return True
        else:
            return False
        
def check_whitelist(message):
    chat_id = message.chat.id
    if chat_id not in whitelist:
        bot.reply_to(message, "Привет! Чтобы использовать, разверни свою копию. Исходники тут https://github.com/ShockThunder/ebenevo-bot")
        raise SystemError("ПОПЫТКА ИСПОЛЬЗОВАНИЯ В ДРУГОМ ЧАТЕ") 


@bot.message_handler(commands=["start"])
def start(message):
    check_whitelist(message)
    bot.reply_to(message, "Привет! Я бот для управления чатом. Напиши /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def help(message):
    check_whitelist(message)
    bot.reply_to(message, "/kick - кикнуть пользователя\n/mute - замутить пользователя на определенное время\n/unmute - размутить пользователя\n/warn - выдать предупреждение\n/unwarn - снять предупреждение\n/checkwarns - узнать количество варнов пользователя\n/ban - забанить")

@bot.message_handler(commands=['kick'])
def kick_user(message):
    check_whitelist(message)
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
            
            # Анбан убирает пользователя из чата
            bot.unban_chat_member(message.chat.id, user_id)

            # Отправляем сообщение с ником и локальным изображением
            with open('./images/kick.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был кикнут.")

                  #шлем сообщение в админский канал  
            bot.send_message(admin_channel_id, f"🔴 #КИК\n"
                                                f"• Кто: {message.reply_to_message.from_user.full_name} [{message.reply_to_message.from_user.id}]\n"
                                                f"• Группа: {message.chat.title} [{message.chat.id}]\n")
            
            # убираем из бд тегов
            who_game_db.remove(query.user_id == user_id)    

        except Exception as e:
            bot.reply_to(message, f"Не удалось кикнуть пользователя: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, которого хотите кикнуть.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    check_whitelist(message)
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

            # убираем из бд тегов
            who_game_db.remove(query.user_id == user_id) 
            
        except Exception as e:
            bot.reply_to(message, f"Не удалось забанить пользователя: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, которого хотите забанить.")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    check_whitelist(message)
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
    check_whitelist(message)
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
    check_whitelist(message)
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

@bot.message_handler(commands=['checkwarns'])
def check_warns(message):
    check_whitelist(message)
    # Проверяем, указано ли сообщение с ID пользователя
    if message.reply_to_message:
        # Проверяем, является ли пользователь администратором    
        if not is_admin(message):
            bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
            return
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

@bot.message_handler(commands=['kicklist'])
def inactive_users(message):
    if not is_admin(message):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return
    
    # Получаем текущую дату
    current_time = int(time())
    two_weeks_ago = current_time - 14 * 24 * 60 * 60

    # Запрос к базе данных
    inactive_users_list = saved_messages_db.search(query.timestamp < two_weeks_ago)

    if inactive_users_list:
        response = "Пользователи, которые не писали более двух недель:\n"
        for user in inactive_users_list:
            last_seen = datetime.fromtimestamp(user['timestamp']).strftime('%Y-%m-%d %H:%M')
            response += f"Пользователь: [{user['first_name']}](tg://user?id={user['user_id']}), Ссылка на последнее сообщение: {user['message_link']}, Дата: {last_seen}\n"
    else:
        response = "Нет пользователей, которые не писали более двух недель."

    bot.reply_to(message, response, parse_mode='Markdown')