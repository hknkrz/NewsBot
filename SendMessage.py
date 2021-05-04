import sqlite3
from TextAnalysis import word_counter


URL = 'https://interfax.ru'


def new_docs(quantity):
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        iteration = 0
        result = dict()
        for element in cur.execute(f"SELECT topic_name,stories FROM topics ORDER BY upd_time DESC"):
            if iteration >= int(quantity):
                break
            result[element[0]] = element[1].split('\n')[-2]
            iteration += 1
        return result


def help():
    pass


def new_topics(quantity):
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        iteration = 0
        result = dict()
        for element in cur.execute(f"SELECT topic_name,link FROM topics ORDER BY upd_time DESC"):
            if iteration >= int(quantity):
                break
            result[element[0]] = URL + element[1]
            iteration += 1
        return result


def topic(name):
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        iteration = 0
        result = dict()
        for element in cur.execute(f"SELECT stories FROM topics WHERE topic_name = '{str(name)}'"):
            if iteration >= 5:
                break
            result[str(name)] = '\n'.join(element[0].split('\n')[-7:-2])
            iteration += 1
        return result


def describe_doc(link):
    info = word_counter(link)
    return {**info[0], **info[1]}


def get_tags(link):
    info = word_counter(link)
    return {info[3]: info[2]}


def words(link):
    info = word_counter(link)
    return {"Возможные ключевые слова": info[4]}