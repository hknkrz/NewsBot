import telebot
from telebot.util import async_dec
import time

from Parser import parse_stories
from SendMessage import new_docs, new_topics, topic, describe_doc, words, get_tags

bot = telebot.TeleBot('1786516962:AAHcmmfEn060vldOLtA_B5lYZZM-hs82UyE')

command_dict = {"/new_docs": new_docs, "/new_topics": new_topics, "/topic": topic, "/describe_doc": describe_doc,
                "/get_tags": get_tags, "/words": words}


@async_dec()
def re_parse():
    starttime = time.time()
    while True:
        parse_stories()
        time.sleep(150.0 - ((time.time() - starttime) % 150.0))


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    command = message.text.split()
    if command[0] == '/help':
        bot.send_message(message.from_user.id, "/new_docs <N> - показать N самых свежих новостей")
        bot.send_message(message.from_user.id, "/new_topics <N> - показать N самых свежих тем")
        bot.send_message(message.from_user.id,
                         "/topic <topic_name> - показать описание темы и заголовки 5 самых свежих новостей в этой теме")
        bot.send_message(message.from_user.id,
                         "/describe_doc <link> - показать частоту слов и распределение слов по длинам")
        bot.send_message(message.from_user.id, "/get_tags <link> - показать теги статьи")
        bot.send_message(message.from_user.id, "/words <link> - показать ключевые слова к статье")


    elif command[0] in command_dict.keys():
        if len(command) < 2:
            bot.send_message(message.from_user.id,
                             "Invalid arguments\n write /help to get a information about arguments for function" +
                             command[0])
        else:

            args = command[1:]
            result = command_dict[command[0]](*args)
            message_to_usr = ''
            for element in result.keys():
                message_to_usr += str(element) + ':\n' + str(result[element]) + '\n'
            bot.send_message(message.from_user.id, message_to_usr)
    else:
        bot.send_message(message.from_user.id, "Invalid function\n write /help to get a list of possible functions")


re_parse()
bot.polling(none_stop=True, interval=0)
