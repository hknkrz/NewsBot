from bs4 import BeautifulSoup
import collections
import requests

FIRST_40_WORDS = 40


def word_counter(link):
    # Частотный анализ текста
    tag_str = ''
    word_dict = collections.Counter()
    response = requests.get(link)

    soup = BeautifulSoup(response.content.decode('windows-1251', 'ignore'), 'lxml')
    text = soup.find('article', itemprop='articleBody')
    header = soup.find('h1', itemprop='headline').get_text()
    tag_bar = soup.find('div', class_='textMTags')
    for tag in tag_bar.find_all('a'):
        tag_str += tag.get_text() + '\n'

    for element in text.find_all('p'):
        for word in element.get_text().split():
            word_dict[word] += 1
    len_dict = len_counter(word_dict)
    words = popular_words(word_dict)
    return word_dict, len_dict, tag_str, header, words


def len_counter(word_dict):
    # Распределение слов по длинам
    len_dict = collections.Counter()
    for key in word_dict.keys():
        len_dict[len(key)] += word_dict[key]
    return len_dict


def popular_words(word_dict):
    # Ключевые слова статьи
    words = []
    for key in word_dict.most_common(FIRST_40_WORDS):
        if len(words) > 3:
            break
        if len(key[0]) > 5:
            words.append(key[0])
    return '\n'.join(words)
