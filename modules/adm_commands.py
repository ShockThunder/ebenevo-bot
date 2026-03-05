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


def send_long_message(bot, message, text, parse_mode=None):
    MAX_LEN = 4096
    for i in range(0, len(text), MAX_LEN):
        part = text[i:i+MAX_LEN]
        bot.reply_to(message, part, parse_mode=parse_mode)

def remove_user_from_all_databases(user_id):
    """
    Удаляет пользователя из всех баз данных
    """
    try:
        # Удаляем из who_game_db
        who_game_db.remove(query.user_id == user_id)
        
        # Удаляем из saved_messages_db
        saved_messages_db.remove(query.user_id == user_id)
        
        # Удаляем из основной базы с предупреждениями
        db.remove(query.id == user_id)
        
        print(f"Пользователь {user_id} успешно удален из всех баз данных")
        
    except Exception as e:
        print(f"Ошибка при удалении пользователя {user_id} из баз данных: {e}")

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
            try:
                with open('./images/kick.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был кикнут.")
            except FileNotFoundError:
                bot.reply_to(message, f"Пользователь @{username} был кикнут.")
            except Exception as e:
                bot.reply_to(message, f"Пользователь @{username} был кикнут. (Ошибка загрузки изображения: {e})")

                  #шлем сообщение в админский канал  
            bot.send_message(admin_channel_id, f"🔴 #КИК\n"
                                                f"• Кто: {message.reply_to_message.from_user.full_name} [{message.reply_to_message.from_user.id}]\n"
                                                f"• Группа: {message.chat.title} [{message.chat.id}]\n")
            
            # убираем из всех баз данных
            remove_user_from_all_databases(user_id)    

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
            try:
                with open('./images/ban.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был забанен.")
            except FileNotFoundError:
                bot.reply_to(message, f"Пользователь @{username} был забанен.")
            except Exception as e:
                bot.reply_to(message, f"Пользователь @{username} был забанен. (Ошибка загрузки изображения: {e})")

            #шлем сообщение в админский канал
            bot.send_message(admin_channel_id, f"🔴 #БАН\n"
                                      f"• Кто: {message.reply_to_message.from_user.full_name} [{message.reply_to_message.from_user.id}]\n"
                                      f"• Группа: {message.chat.title} [{message.chat.id}]\n")

            # убираем из всех баз данных
            remove_user_from_all_databases(user_id) 
            
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
                # Валидация входных данных
                if duration < 1:
                    bot.reply_to(message, "Время должно быть положительным числом.")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Максимальное время - 1 день.")
                    return
                if duration > 10080:  # 7 дней
                    bot.reply_to(message, "Слишком большое время для мута.")
                    return
            except ValueError:
                bot.reply_to(message, "Неправильный формат времени. Используйте число минут.")
                return
            except Exception as e:
                bot.reply_to(message, f"Ошибка при обработке времени: {e}")
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
    
    # Обновляем информацию о пользователе, который выдает предупреждение
    from modules.party import update_user_info_in_all_databases
    update_user_info_in_all_databases(message.from_user)
    
    if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            
            # Обновляем информацию о пользователе, которому выдается предупреждение
            update_user_info_in_all_databases(message.reply_to_message.from_user)
            
            try:
                user_data = db.get(query.id == user_id)
                if user_data:
                    warnings_count = user_data.get('warnings', 0) + 1
                    db.update({'warnings': warnings_count}, query.id == user_id)        
                else:
                    db.insert({'id': user_id, 'warnings': 1})
                    warnings_count = 1
            except Exception as e:
                bot.reply_to(message, f"Ошибка при работе с базой данных: {e}")
                return

            if warnings_count >= 3:
                bot.ban_chat_member(message.chat.id, user_id)
                # Отправляем сообщение с ником и локальным изображением
                try:
                    with open('./images/ban.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} был кикнут за превышение количества предупреждений.")
                except FileNotFoundError:
                    bot.reply_to(message, f"Пользователь @{username} был кикнут за превышение количества предупреждений.")
                except Exception as e:
                    bot.reply_to(message, f"Пользователь @{username} был кикнут за превышение количества предупреждений. (Ошибка загрузки изображения: {e})")
                db.remove(query.id == user_id)
            else:
                try:
                    with open('./images/warn.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{username} получил предупреждение. Всего предупреждений: {warnings_count}/3")
                except FileNotFoundError:
                    bot.reply_to(message, f"Пользователь @{username} получил предупреждение. Всего предупреждений: {warnings_count}/3")
                except Exception as e:
                    bot.reply_to(message, f"Пользователь @{username} получил предупреждение. Всего предупреждений: {warnings_count}/3 (Ошибка загрузки изображения: {e})")

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
    
    # Обновляем информацию о пользователе, который снимает предупреждение
    from modules.party import update_user_info_in_all_databases
    update_user_info_in_all_databases(message.from_user)
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        
        # Обновляем информацию о пользователе, которому снимается предупреждение
        update_user_info_in_all_databases(message.reply_to_message.from_user)
        
        try:
            user_data = db.get(query.id == user_id)
            
            if user_data:
                warnings_count = user_data.get('warnings', 0)
                if warnings_count > 0:
                    warnings_count -= 1
                    db.update({'warnings': warnings_count}, query.id == user_id)
                    
                    if warnings_count == 0:
                        # Если предупреждений больше нет, можно удалить пользователя из базы
                        db.remove(query.id == user_id)
                        try:
                            with open('./images/unwarn.jpg', 'rb') as photo:
                                bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{message.reply_to_message.from_user.username} больше не имеет предупреждений.")
                        except FileNotFoundError:
                            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} больше не имеет предупреждений.")
                        except Exception as e:
                            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} больше не имеет предупреждений. (Ошибка загрузки изображения: {e})")
                    else:
                        try:
                            with open('./images/light_unwarn.jpg', 'rb') as photo:
                                bot.send_photo(message.chat.id, photo=photo, caption=f"Пользователь @{message.reply_to_message.from_user.username} теперь имеет {warnings_count} предупреждений.")
                        except FileNotFoundError:
                            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} теперь имеет {warnings_count} предупреждений.")
                        except Exception as e:
                            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} теперь имеет {warnings_count} предупреждений. (Ошибка загрузки изображения: {e})")
                else:
                    bot.reply_to(message, f"У пользователя @{message.reply_to_message.from_user.username} нет предупреждений.")
            else:
                bot.reply_to(message, "Пользователь не имеет предупреждений.")
        except Exception as e:
            bot.reply_to(message, f"Ошибка при работе с базой данных: {e}")
            return
    else:
        bot.reply_to(message, "Пожалуйста, ответьте на сообщение пользователя, у которого хотите снять предупреждение.")

@bot.message_handler(commands=['checkwarns'])
def check_warns(message):
    check_whitelist(message)
    
    # Обновляем информацию о пользователе, который проверяет предупреждения
    from modules.party import update_user_info_in_all_databases
    update_user_info_in_all_databases(message.from_user)
    
    # Проверяем, указано ли сообщение с ID пользователя
    if message.reply_to_message:
        # Проверяем, является ли пользователь администратором    
        if not is_admin(message):
            bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
            return
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        
        # Обновляем информацию о пользователе, у которого проверяются предупреждения
        update_user_info_in_all_databases(message.reply_to_message.from_user)
    else:
        # Если команда не была вызвана в ответ на сообщение, покажем свои варны
        user_id = message.from_user.id
        username = message.from_user.username
    
    try:
        user_data = db.get(query.id == user_id)
        
        if user_data:
            warnings_count = user_data.get('warnings', 0)
            bot.reply_to(message, f"Пользователь @{username} имеет {warnings_count} предупреждений.")
        else:
            bot.reply_to(message, f"У пользователя @{username} нет предупреждений.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при получении информации о предупреждениях: {e}")

@bot.message_handler(commands=['kicklist'])
def inactive_users(message):
    if not is_admin(message):
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    chat_id = message.chat.id

    # Получаем текущую дату
    current_time = int(time())
    two_weeks_ago = current_time - 14 * 24 * 60 * 60

    # Запрос к базе данных
    try:
        inactive_users_list = saved_messages_db.search(query.timestamp < two_weeks_ago)

        if inactive_users_list:
            # Оставляем только тех, кто ещё в чате (не left и не kicked)
            still_in_chat = []
            for user in inactive_users_list:
                try:
                    member = bot.get_chat_member(chat_id, user['user_id'])
                    if member.status in ('left', 'kicked'):
                        # Удаляем из БД — вышел из чата, не показываем в киклисте
                        saved_messages_db.remove(query.user_id == user['user_id'])
                    else:
                        still_in_chat.append(user)
                except Exception:
                    # Пользователь не найден в чате (уже вышел) — удаляем из БД
                    saved_messages_db.remove(query.user_id == user['user_id'])
                    continue

            if still_in_chat:
                response = "Пользователи, которые не писали более двух недель:\n"
                for user in still_in_chat:
                    try:
                        last_seen = datetime.fromtimestamp(user['timestamp']).strftime('%Y-%m-%d %H:%M')
                        response += f"Пользователь: [{user['first_name']}](tg://user?id={user['user_id']}), Ссылка на последнее сообщение: {user['message_link']}, Дата: {last_seen}\n"
                    except (KeyError, ValueError, TypeError):
                        continue
                send_long_message(bot, message, response, 'Markdown')
            else:
                bot.reply_to(message, "Нет пользователей, которые не писали более двух недель (или они уже вышли из чата).")
        else:
            bot.reply_to(message, "Нет пользователей, которые не писали более двух недель.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка при получении списка неактивных пользователей: {e}")