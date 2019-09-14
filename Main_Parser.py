from nltk.corpus import stopwords
from nltk.corpus import RegexpTokenizer
import requests
from bs4 import BeautifulSoup
import nltk
import functools

def get_soup(link):
    """ Получаем soup с ссылки
    :param link: ссылка
    :return: soup
    """
    con = requests.get(link).content
    soup = BeautifulSoup(con, "lxml")
    return soup

s = get_soup('https://secretmag.ru/news')
soup = s.find_all('div',{'class':'jsx-755400851 _345R9Vbg0tNxP1XCLWC2zw headline'})
title = [] # названия статей лежат тут
for a in soup:
    title += [a.get_text()]

# for a, b in enumerate(title):
#     print(a , b)

soup2 = s.find_all('a',{'class':'jsx-2447512944 link _2PyABjMPMWl0WEOYy2y3Fp'}) # нашел объекты в которых лежат ссылки

links = [] # все ссылки сдесь
for a in soup2:
    links += ['https://secretmag.ru/' + a.get('href')]

def get_text_on_page(link):
    soup = get_soup(link)
    page = soup.find_all('p', {'class':'jsx-3332198469'})
    text = []
    for a in page:
        text += [a.get_text()]
    text = text[:-1]
    string = ''
    for a in text:
        string += a
    return string

text_all_pages = [] # с помощью функции выше собрал текст со всех страниц
for a in links:
    text_all_pages.append(get_text_on_page(a))










import wget

udpipe_url = 'http://rusvectores.org/static/models/udpipe_syntagrus.model'
text_url = 'http://rusvectores.org/static/henry_sobolya.txt'

modelfile = wget.download(udpipe_url)
textfile = wget.download(text_url)
#
from ufal.udpipe import Model, Pipeline

def tag_ud(text='Текст нужно передать функции в виде строки!', modelfile='udpipe_syntagrus.model'):
    model = Model.load(modelfile)
    pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
    processed = pipeline.process(text) # обрабатываем текст, получаем результат в формате conllu
    output = [l for l in processed.split('\n') if not l.startswith('#')] # пропускаем строки со служебной информацией
    tagged = [w.split('\t')[2].lower() + '_' + w.split('\t')[3] for w in output if w] # извлекаем из обработанного текста лемму и тэг
    tagged_propn = []
    propn  = []
    for t in tagged:
        if t.endswith('PROPN'):
            if propn:
                propn.append(t)
            else:
                propn = [t]
        else:
            if len(propn) > 1:
                name = '::'.join([x.split('_')[0] for x in propn]) + '_PROPN'
                tagged_propn.append(name)
            elif len(propn) == 1:
                tagged_propn.append(propn[0])
            tagged_propn.append(t)
            propn = []
    return tagged_propn
#
text = open(textfile, 'r', encoding='utf-8').read()
processed_ud = tag_ud(text=text, modelfile=modelfile)
# print(processed_ud[:30])
#
from pymystem3 import Mystem

def tag_mystem(text='Текст нужно передать функции в виде строки!'):
    m = Mystem()
    processed = m.analyze(text)
    tagged = []
    for w in processed:
        try:
            lemma = w["analysis"][0]["lex"].lower().strip()
            pos = w["analysis"][0]["gr"].split(',')[0]
            pos = pos.split('=')[0].strip()
            tagged.append(lemma.lower() + '_' + pos)
        except KeyError:
            continue # я здесь пропускаю знаки препинания, но вы можете поступить по-другому
    return tagged
#
# processed_mystem = tag_mystem(text=text)
# print(processed_mystem[:10])
#
import requests
import re

url = 'https://raw.githubusercontent.com/akutuzov/universal-pos-tags/4653e8a9154e93fe2f417c7fdb7a357b7d6ce333/ru-rnc.map'

mapping = {}
r = requests.get(url, stream=True)
for pair in r.text.split('\n'):
    pair = re.sub('\s+', ' ', pair, flags=re.U).split(' ')
    if len(pair) > 1:
        mapping[pair[0]] = pair[1]

print(mapping)
#
def tag_mystem(text='Текст нужно передать функции в виде строки!'):
    m = Mystem()
    processed = m.analyze(text)
    tagged = []
    for w in processed:
        try:
            lemma = w["analysis"][0]["lex"].lower().strip()
            pos = w["analysis"][0]["gr"].split(',')[0]
            pos = pos.split('=')[0].strip()
            if pos in mapping:
                tagged.append(lemma + '_' + mapping[pos]) # здесь мы конвертируем тэги
            else:
                tagged.append(lemma + '_X') # на случай, если попадется тэг, которого нет в маппинге
        except KeyError:
            continue # я здесь пропускаю знаки препинания, но вы можете поступить по-другому
    return tagged
#
# processed_mystem = tag_mystem(text=text)
# print(processed_mystem[:10])

# -- - - -  -- -- - -- -- - -- - -- - 2 Этап
import sys
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#
model_url = 'http://rusvectores.org/static/models/rusvectores4/RNC/ruscorpora_upos_skipgram_300_5_2018.vec.gz'
modelfile = wget.download(model_url)
m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.Word2Vec.load(m)
#
import gensim.downloader as api

ruscorpora_model = api.load("word2vec-ruscorpora-300")

#
model.init_sims(replace=True)
#
words = ['день_NOUN', 'ночь_NOUN', 'человек_NOUN', 'семантика_NOUN', 'студент_NOUN', 'студент_ADJ']
#
for word in words:
    # есть ли слово в модели? Может быть, и нет
    if word in model:
        print(word)
        # выдаем 10 ближайших соседей слова:
        for i in model.most_similar(positive=[word], topn=10):
            # слово + коэффициент косинусной близости
            print(i[0], i[1])
        print('\n')
    else:
        # Увы!
        print(word + ' is not present in the model')
print(model.similarity('человек_NOUN', 'обезьяна_NOUN'))

print(model.doesnt_match('яблоко_NOUN груша_NOUN виноград_NOUN банан_NOUN лимон_NOUN картофель_NOUN'.split()))

print(model.most_similar(positive=['пицца_NOUN', 'россия_NOUN'], negative=['италия_NOUN'])[0][0])
