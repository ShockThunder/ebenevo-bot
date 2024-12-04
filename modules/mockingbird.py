from core import ebenevobot

bot = ebenevobot.bot

keywords = {
    "да": "пизда",
    "нет": "пидора ответ",
    "молодец": "соси конец"
}

@ebenevobot.bot.message_handler(func=lambda message: True)
def respond_to_keywords(message):
    # Проверяем, содержит ли сообщение ключевые слова
    for keyword, response in keywords.items():
        if keyword == message.text.lower():
            if(keyword == "молодец" and message.from_user.id == 80207393):
                bot.reply_to(message, "спасибо")
            else:
                bot.reply_to(message, response)
            break  # Выходим из цикла после первого совпадения 