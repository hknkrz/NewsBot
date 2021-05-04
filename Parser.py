import requests
from bs4 import BeautifulSoup
import sqlite3

URL = 'https://interfax.ru'
NEED_UPD_FLAG = 1
NO_UPD_FLAG = 0
NEED_CREATE_FLAG = 2
NULL_TIME = None


def parse_stories():
    upd_time_dict = create_upd_dict()
    response = requests.get(URL + '/story/')
    soup = BeautifulSoup(response.text, 'lxml')

    items = soup.find('div', class_='newsmain')
    page_board = soup.find('div', class_='allPNav')
    pages = page_board.find_all('a')
    last_page = pages[len(pages) - 1]['href'][12:]
    itr = 0
    for page in range(1, int(last_page) + 1):
        # Парсинг 10 первых страниц
        if itr == 10:
            break
        cur_url = URL + '/story/page_' + str(page)
        response = requests.get(cur_url)
        soup = BeautifulSoup(response.content.decode('windows-1251', 'ignore'), 'lxml')
        items = soup.find_all('div', class_='allStory')
        for item in items:
            topics = item.find_all('div', recursive=False)
            for topic in topics:
                link = topic.find('a')['href']
                if link[:6] != '/story':
                    continue
                time = topic.find('time')['datetime']
                name = topic.find('a')['title']

                if name in upd_time_dict.keys():
                    if upd_time_dict[name][0] != str(time):
                        upd_time_dict[name][0] = str(time)
                        upd_time_dict[name][1] = NEED_UPD_FLAG
                        upd_time_dict[name][2] = parse_topics(link, time)


                    else:
                        pass
                else:
                    pass
                    upd_time_dict[name] = [str(time), NEED_CREATE_FLAG, parse_topics(link, NULL_TIME), link]
        itr += 1

    update_db(upd_time_dict)
    return


def update_db(update_dict):
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS topics(topic_name PRIMARY KEY,upd_time TEXT,stories TEXT,link TEXT )""")
        for key in update_dict.keys():
            if update_dict[key][1] == NO_UPD_FLAG:
                continue
            elif update_dict[key][1] == NEED_UPD_FLAG:
                for i in cur.execute(f"SELECT stories FROM topics WHERE topic_name = '{key}'"):
                    substr = i[0]
                cur.execute(
                    f"UPDATE topics SET stories = {substr + update_dict[key][2]}")
                cur.execute(
                    f"UPDATE topics SET upd_time = {substr + update_dict[key][0]}")

            else:
                cur.execute(f"INSERT INTO topics VALUES (?,?,?,?)",
                            (key, update_dict[key][0], update_dict[key][2], update_dict[key][3]))

                pass
        conn.commit()


def parse_topics(link, time):
    result = []
    response = requests.get(URL + link)
    soup = BeautifulSoup(response.text, 'lxml')
    page_board = soup.find('div', class_='allPNav')
    if not page_board:
        last_page = 1
    else:
        pages = page_board.find_all('a')
        last_page = pages[len(pages) - 1]['href'].split('_')[1]
    for page in range(1, int(last_page) + 1):
        stories = parse_page(link, '/page_' + str(page))
        for story in stories:
            if story.find('a'):
                if time and str(story.find('time')['datetime']) == time:
                    return result

                result.append(URL + story.find('a')['href'])
    return '\n'.join(list(reversed(result)))


def parse_page(link, page):
    cur_url = URL + link + str(page)
    response = requests.get(cur_url)
    soup = BeautifulSoup(response.text, 'lxml')
    story_list = soup.find('div', class_='storyList')
    return story_list.find_all('div', recursive=False)


def create_upd_dict():
    update_time = dict()
    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS topics(topic_name PRIMARY KEY,upd_time TEXT,stories TEXT,link TEXT )""")

        conn.commit()

        for topic in cur.execute("SELECT topic_name,upd_time FROM topics"):
            update_time[topic[0]] = [topic[1], NO_UPD_FLAG, '', '']
        return update_time

