import requests
import sqlite3
from TextAnalysis import word_counter

URL = 'https://interfax.ru'
KEY_WORD_QUANTITY = 4


def new_docs(quantity):
    if not quantity.isnumeric():
        raise Exception('Excepted integer value')
    # Отправить quantity свежих новостей
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        result = {}
        for element in enumerate(cur.execute("SELECT topic_name,stories FROM topics ORDER BY upd_time DESC")):
            if element[0] >= int(quantity):
                break
            result[element[1][0]] = element[1][1].split('\n')[-1]
        return result


def new_topics(quantity):
    # Отправить quantity актуальных разделов
    if not quantity.isnumeric():
        raise Exception('Excepted integer value')
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        result = {}
        for element in enumerate(cur.execute("SELECT topic_name,link FROM topics ORDER BY upd_time DESC")):
            if element[0] >= int(quantity):
                break
            result[element[1][0]] = URL + element[1][1]
        return result


def topic(name):
    # Отправить 5 свежих новостей из раздела name
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        result = {}
        for element in enumerate(cur.execute(f"SELECT stories FROM topics WHERE topic_name = '{str(name)}'")):
            if element[0] >= 5:
                break
            result[str(name)] = '\n'.join(element[1][0].split('\n')[-6:-1])
        if not len(result):
            raise Exception('Wrong topic name')
        return result


def describe_doc(link):
    try:
        requests.get(link)
    except Exception:
        raise Exception('Excepted correct link')
    # Отправить статистику по статье
    info = word_counter(link)
    return {**info[0], **info[1]}


def get_tags(link):
    try:
        requests.get(link)
    except Exception:
        raise Exception('Excepted correct link')
    # Отправить теги статьи
    info = word_counter(link)
    return {info[3]: info[2]}


def words(link):
    try:
        requests.get(link)
    except Exception:
        raise Exception('Excepted correct link')
    # Отправить ключевые слова статьи
    info = word_counter(link)
    return {'Возможные ключевые слова': info[KEY_WORD_QUANTITY]}
