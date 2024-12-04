from core import ebenevobot
from data import db_handler

bot = ebenevobot.bot
admin_channel_id = ebenevobot.report_channel

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        # Приветствуем нового участника
        # Отправляем сообщение с ником и локальным изображением
        with open('./images/welcome.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo, caption=f"Приветствую, {new_member.first_name}!\nМы рады видеть тебя в нашем чате 🍀\n\nРасскажи нам немного о себе:\nКак тебя можно звать?\nСколько тебе лет?\nКем работаешь и чем любишь увлекаться?\n\nТак мы сможем помочь тебе быстрее адаптироваться 🐙")
    
    #шлем сообщение в админский канал
    bot.send_message(admin_channel_id, f"➕ #НОВЫЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                      f"• Кто: {new_member.full_name} [{new_member.id}]\n"
                                      f"• Группа: {message.chat.title} [{message.chat.id}]\n")

@bot.message_handler(content_types=['left_chat_member'])
def user_chat_member_update(message):
    left_member = message.left_chat_member
    with open('./images/left.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo=photo, caption=f"Прощай, {left_member.first_name}! Мы будем по тебе скучать! 😢")
    
    #шлем сообщение в админский канал
    bot.send_message(admin_channel_id, f"➖ #УШЕДШИЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                  f"• Кто: {message.left_chat_member.full_name} [{message.left_chat_member.id}]\n"
                                  f"• Группа: {message.chat.title} [{message.chat.id}]\n")



@bot.message_handler(content_types=['chat_member'])
def chat_member_update(message):
    new_member = message.chat_member.new_chat_member
    old_member = message.chat_member.old_chat_member

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

        elif new_member.status == 'left':
            left_member = message.left_chat_member
            with open('./images/left.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption=f"Прощай, {left_member.first_name}! Мы будем по тебе скучать! 😢")
            bot.send_message(admin_channel_id, f"➖ #УШЕДШИЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                            f"• Кто: {message.left_chat_member.full_name} [{message.left_chat_member.id}]\n"
                                            f"• Группа: {message.chat.title} [{message.chat.id}]\n")