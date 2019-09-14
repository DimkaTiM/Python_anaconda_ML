"""
Hello world 2
"""
import os
import pickle
import collections
from nltk.corpus import stopwords
from nltk.corpus import RegexpTokenizer
import pymorphy2
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


def get_soup(link):
    """ Получаем СУП с сылки
    :param link: ссылка
    :return: суп
    """
    con = requests.get(link).content
    soup = BeautifulSoup(con, "lxml")
    return soup


def compute_tf(text):
    """ Подсчет встречаемости слов
    :param text: текс
    :return: встречаемсоть
    """
    tf_text = collections.Counter(text)
    for i in tf_text:
        tf_text[i] = tf_text[i] / float(len(text))
    return tf_text


def word_list(text):
    """ Получаем словарь
    :param text:
    :return: словарь с макс встречаемостью в статье
    """
    stop_words = stopwords.words("russian")
    morph = pymorphy2.MorphAnalyzer()
    words = RegexpTokenizer(r'\w+').tokenize(text)

    filtered_sentence = [w for w in words if not w in stop_words]
    sentence = [morph.parse(ent) for ent in filtered_sentence]
    result = [ent[0].normal_form for ent in sentence if ent[0].tag.POS == "NOUN"]
    computed_result = compute_tf(result)
    return computed_result


def get_page_links(obj):
    """Все ссылки со страницы
    :param obj: суп
    :return: ссылки со страницы
    """
    links = []
    for lin in obj:
        text = "https://burdastyle.ru"
        links.append(text + lin['href'])
    return links


def get_page_text(link):
    maxwords = 15
    """Удаляем все лишние знаки из слов
    :param link: ссылка на статью
    :return: текст без изменений
    """
    soup = get_soup(link)
    obj = soup.find('div', {'class': ['article-listing', 'article-page item layout-lg']})\
        .find_all("a", {'class' : 'image'})

    links = get_page_links(obj)

    doroy = []
    qut = []
    for lin in links:
        soup = get_soup(lin)
        obj = [ent.text.replace('\xa0', ' ') for ent in soup.find('div', \
        {'id': 'tools'}).find_all('p') if ent.text]
        doroy.append(obj)

    for ent in doroy:
        tmp = " ".join(ent)
        qut.append(tmp)


    stop = stopwords.words("russian")
    alltext = []
    stop = stop + ["х", 'хх', 'м', 'е'] + [str(i) for i in range(3000)]
    count = 0
    for text in qut:
        tokenizer = RegexpTokenizer(r"\w+")
        words = tokenizer.tokenize(text.lower())
        keywords = [w for w in words if w not in stop]
        sss = ""
        for ent in keywords:
            sss = sss + ' ' + ent
        alltext.append(sss)
        count = count + 1

    alldict = []
    count = 0
    for ent in alltext:
        alldict.append([links[count], list(word_list(ent))[:maxwords]])
        count = count + 1
    return alldict


def get_all_text(linkk):
    PAGES_COUNT = 20
    """Вызов подфункций, сбор текста, по всем страницам
    :param linkk: главный сайт
    :return: весь текст без мусора - только слова
    """
    allalltext = []
    count = 0
    for ent in range(1, PAGES_COUNT):
        string = "?page="
        link = linkk + string + str(ent)
        allalltext.append(get_page_text(link))
        print(str(count), get_page_text(link))
        count = count + 1
    return allalltext


def get_all_all_links_of_site(linkk):
    """Получение все сылок со всех страниц и всех статей
    :param linkk: код сайта
    :return: список страниц, в котрохый список ссылок на стаьи
    """
    allalllinks = []
    for ent in range(1, 168):
        string = "?page="
        link = linkk + string + str(ent)
        soup = get_soup(link)
        obj = soup.find('div', {'class': ['article-listing', 'article-page item layout-lg']}) \
            .find_all("a", {'class': 'image'})
        links = get_page_links(obj)
        allalllinks.append(links)
        return allalllinks


def write_in(file_name, input):
    """Запись в файл
    :param file_name: файл в стринге
    :param input: что записывать
    :return: NO, запись произведена
    """
    PATH = os.path.abspath('.')
    with open(PATH + file_name, "wb") as read:
        pickle.dump(input, read)


def write_out(file_name):
    """Вывод из файла, все будет храниться в output
    :param file_name: Файл из которого считывают
    :param output: переменная куда происходит считывание
    :return:
    """
    r = os.path.abspath('.')
    with open(r + file_name, 'rb') as file2:
        out_put = pickle.load(file2)
    return out_put


def recomindation(alltext):
    """Рекомендация по всему тексту
    :param alltext: струтура список, где в элементе лежит ссылка и ключевые слова
    :return: списко словарей {ссылка: {рекомендация: ключевые слова}
    """
    resume = []
    for i in range(0, len(alltext) - 1):
        A = set(alltext[i][1])
        tmp_list = []
        for j in range(0, len(alltext)):
            if i != j:
                B = set(alltext[j][1])
                intersection = A.intersection(B)
                if len(intersection) > 4:
                    # print(alltext[i][0], alltext[j][0])
                    # print(A, B, intersection, sep='\n')
                    tmp_list.append({alltext[j][0]: intersection})
                    conn = create_connection("/Users/dimatimohin/sqlite/pythonsqlite.db")
                    insert_data(conn, 'recommendations2', alltext[i][0], intersection, alltext[j][0])
        if tmp_list:
            resume.append({alltext[i][0]: tmp_list})
    return resume


def create_connection(db_file):
    """Соединение с базой SQL
    :param db_file:
    :return:
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_table_data(conn, table_name):
    """Получить всю таблицу
    :param conn: коннектор
    :param table_name: имя таблицы
    """
    cursor = conn.cursor()
    sql = "SELECT * FROM " + table_name
    cursor.execute(sql)
    return cursor.fetchall()


def insert_data(conn, table_name, article, keywords, recomend_article):
    """ вставить строку в таблицу
    :param conn: коннектор
    :param table_name: имя таблицы
    """
    cursor = conn.cursor()
    sql = "INSERT INTO " + table_name + " (article, keywords, article_recommendation) VALUES (?, ?, ?)"
    cursor.execute(sql, (str(article), str(keywords), str(recomend_article)))
    conn.commit()
    return "inserted"


def delete_data(conn, table_name):
    """ Удалить все данные таблицы
    :param conn: коннектор
    :param table_name: какую базу удалить
    """
    cursor = conn.cursor()
    sql = "DELETE FROM " + table_name
    cursor.execute(sql)
    conn.commit()
    return "all data deleted"


data_base = "/Users/dimatimohin/sqlite/pythonsqlite.db"
conn = create_connection("/Users/dimatimohin/sqlite/pythonsqlite.db")
creatable_table1 = "CREATE TABLE IF NOT EXISTS articles (id integer primary key AUTOINCREMENT," \
              " title text, link text, description text, date text, article_text text, author text," \
              " keywords text DEFAULT NULL, category_id integer DEFAULT NULL)"

creatable_table2 = "CREATE TABLE IF NOT EXISTS recommendations2(article text, keywords text, article_recommendation text)"
# create_table(conn, creatable_table1)

create_table(conn, creatable_table2)
a = get_table_data(conn, "recommendations2")
print(a)
delete_data(conn, "recommendations2")



# file1 = "/123.pickle"
# link = 'https://burdastyle.ru/stati/'
# alltext = get_all_text(link)
# write_in(file1, alltext)


file1 = "/123.pickle"
file2 = "/all_links.pickle"


alltext = write_out(file1)
file1alllinks = write_out(file2)

#запись
# write_in(file1, get_all_text(link))
# write_in(file2, get_all_all_links_of_site(link))






alltext = sum(alltext, [])
resume = recomindation(alltext)







for k, v in enumerate(resume):
    for key, value in v.items():
        print("-----------------------")
        print("                Статья:  " + key)
        for slov in value:
            for kk, vv in  slov.items():
                print("Рекомендованная статья:  " + str(kk))
                print("        Ключевые слова:  " + str(vv))
                print()
# print("5 совпадений по словам для рекомендации")

