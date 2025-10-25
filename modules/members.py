from core import ebenevobot
from modules import db_handler
from modules import adm_commands
from datetime import datetime
from time import time
check_whitelist = adm_commands.check_whitelist

bot = ebenevobot.bot
admin_channel_id = ebenevobot.report_channel
who_game_db = db_handler.who_game_db
saved_messages_db = db_handler.saved_messages_db
query = db_handler.query

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    check_whitelist(message)

    for new_member in message.new_chat_members:
        # Приветствуем нового участника
        # Отправляем сообщение с ником и локальным изображением
        if (new_member.id == 80207393):
            with open('./images/hi.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo)
        else:
            with open('./images/welcome.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption=f"Приветствую, [{new_member.first_name}](tg://user?id={new_member.id})!\nМы рады видеть тебя в нашем чате 🍀\n\nРасскажи нам немного о себе:\nКак тебя можно звать?\nСколько тебе лет?\nКем работаешь и чем любишь увлекаться?\n\nПравила чата читать тут (https://t.me/c/2482107448/48095)\nАнонс мероприятий, барахолка, фото и анкеты мы выкладываем сюда: https://t.me/+nJdcXnmSy-sxYjFi", parse_mode='Markdown')
       
        # Проверка, существует ли пользователь в базе данных
        if not who_game_db.contains(query.user_id == new_member.id):
            # Если пользователь не существует, добавляем его в базу данных
            who_game_db.insert({'user_id': new_member.id, 'username': new_member.username, 'first_name': new_member.first_name, 'last_name': new_member.last_name})
    
    #шлем сообщение в админский канал
    bot.send_message(admin_channel_id, f"➕ #НОВЫЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                      f"• Кто: {new_member.full_name} [{new_member.id}]\n"
                                      f"• Группа: {message.chat.title} [{message.chat.id}]\n")
    user = new_member
    timestamp = int(time())
    saved_messages_db.insert({'user_id': user.id, 'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'message_link': message, 'timestamp': timestamp})
    


@bot.chat_member_handler(func=None)
def chat_member_update(message):
    check_whitelist(message)

    new_member = message.new_chat_member
    old_member = message.old_chat_member

    # Проверяем, если статус изменился
    if new_member.status != old_member.status:
        if new_member.status == 'administrator':
                    bot.send_message(admin_channel_id, f"🟢 #ПОВЫШЕНИЕ_РОЛИ\n"
                                                f"• Кто: {new_member.user.full_name} [{new_member.user.id}]\n"
                                                f"• Новая роль: Администратор\n"
                                                f"• Группа: {message.chat.title} [{message.chat.id}]")
        elif old_member.status == 'administrator':
            bot.send_message(admin_channel_id, f"🔴 #УДАЛЕНИЕ_РОЛИ\n"
                                        f"• Кто: {new_member.user.full_name} [{new_member.user.id}]\n"
                                        f"• Удалена роль: Администратор\n"
                                        f"• Группа: {message.chat.title} [{message.chat.id}]")
            
        elif new_member.status == 'left' and old_member.status != 'kicked':
            if (new_member.user.id == 80207393):
                with open('./images/cry.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo)
            else:
                with open('./images/left.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=f"Прощай, [{new_member.user.first_name}](tg://user?id={new_member.user.id})! Мы будем по тебе скучать! 😢", parse_mode='Markdown')
            
                #шлем сообщение в админский канал
                bot.send_message(admin_channel_id, f"➖ #УШЕДШИЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                            f"• Кто: {new_member.user.full_name} [{new_member.user.id}]\n"
                                            f"• Группа: {message.chat.title} [{message.chat.id}]\n")
                
                # удаляем пользователя из баз (пока есть только who_game)
                who_game_db = db_handler.who_game_db
                query = db_handler.query
                who_game_db.remove(query.user_id == new_member.user.id)
                saved_messages_db.remove(query.user_id == new_member.user_id)
