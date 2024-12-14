from core import ebenevobot
from modules import db_handler

bot = ebenevobot.bot
admin_channel_id = ebenevobot.report_channel

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        # Приветствуем нового участника
        # Отправляем сообщение с ником и локальным изображением
        if (new_member.id == 80207393):
            with open('./images/hi.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo)
        else:
            with open('./images/welcome.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption=f"Приветствую, {new_member.first_name}!\nМы рады видеть тебя в нашем чате 🍀\n\nРасскажи нам немного о себе:\nКак тебя можно звать?\nСколько тебе лет?\nКем работаешь и чем любишь увлекаться?\n\nТак мы сможем помочь тебе быстрее адаптироваться 🐙")
    
    #шлем сообщение в админский канал
    bot.send_message(admin_channel_id, f"➕ #НОВЫЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                      f"• Кто: {new_member.full_name} [{new_member.id}]\n"
                                      f"• Группа: {message.chat.title} [{message.chat.id}]\n")

@bot.chat_member_handler(func=None)
def chat_member_update(message):

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
            
        elif new_member.status == 'left':
            if (new_member.user.id == 80207393):
                with open('./images/cry.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo)
            else:
                with open('./images/left.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption=f"Прощай, {new_member.user.first_name}! Мы будем по тебе скучать! 😢")
            
                #шлем сообщение в админский канал
                bot.send_message(admin_channel_id, f"➖ #УШЕДШИЙ_ПОЛЬЗОВАТЕЛЬ\n"
                                            f"• Кто: {new_member.user.full_name} [{new_member.user.id}]\n"
                                            f"• Группа: {message.chat.title} [{message.chat.id}]\n")
