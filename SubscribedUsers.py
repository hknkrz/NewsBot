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
            if upd_time_dict[name][0] != time:
                upd_time_dict[name][0] = str(time)
                upd_time_dict[name][1] = NEED_UPD_FLAG


    with sqlite3.connect('User.db') as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS topics(topic_name PRIMARY KEY,link TEXT,upd_time TEXT,stories TEXT )""")
        conn.commit()

        for topic in cur.execute("SELECT topic_name,upd_time FROM topics"):
            update_time[topic[0]] = [topic[1], NO_UPD_FLAG, [], '']
        return update_time