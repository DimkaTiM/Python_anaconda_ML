import ner
import wget
import gensim
import requests
import pymorphy2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords, RegexpTokenizer


def get_article_text(link):
    text = ""
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find("div", {"class": "news-text"}).text.replace("\t", "").replace("\r", "").replace("\n", "").replace("\xa0", " ").strip()
    return text


def word_list(text):
    morph = pymorphy2.MorphAnalyzer()
    stop_words = stopwords.words("russian")
    tokenizer = RegexpTokenizer(r'[\w\d]+')
    words = tokenizer.tokenize(text)
    filtered_sentence = [w for w in words if not w in stop_words]
    sentence = [morph.parse(ent) for ent in filtered_sentence]
    result = []
    for ent in sentence:
        if ent[0].tag.POS == "NOUN":
            result.append(ent[0].normal_form)
        elif 'NUMB' in ent[0].tag:
            result.append(ent[0].word)
    return result

def model_init():
    model_url = 'http://rusvectores.org/static/models/rusvectores4/taiga/taiga_upos_skipgram_300_2_2018.vec.gz'
    modelfile = wget.download(model_url)
    m = 'taiga_upos_skipgram_300_2_2018.vec.gz'
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.Word2Vec.load(m)
    model.init_sims(replace=True)
    return model


def get_similar(words):
    s = []
    for ent in words:
        try:
            similar = model.most_similar(ent)
            s.append(similar)
        except:
            s.append(ent)
    return s



model = model_init()

def init(LINK):
    text = get_article_text(LINK)
    words = list(set(word_list(text)))
    entity = []
    for ent in words:
        if ent.isalpha():
            entity.append(ent + "_NOUN")
        else:
            entity.append(ent)
    similar = get_similar(entity)
    return text, words, similar


tmp_str = "http://firrma.ru/projects/reyting_angelov_2016/,http://firrma.ru/data/news/123897/,http://firrma.ru/data/news/98600/,http://firrma.ru/data/news/98713/,http://firrma.ru/data/news/98838/,http://firrma.ru/data/news/99026/,http://firrma.ru/data/news/99477/,http://firrma.ru/data/news/99629/,http://firrma.ru/data/news/99667/,http://firrma.ru/data/news/99626/,http://firrma.ru/data/news/99929/,http://firrma.ru/data/news/100092/,http://firrma.ru/data/news/101173/,http://firrma.ru/data/news/101168/,http://firrma.ru/data/news/101557/,http://firrma.ru/data/news/102446/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102698/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102624/,http://firrma.ru/data/news/102768/,http://firrma.ru/data/news/103066/,http://firrma.ru/data/news/103069/,http://firrma.ru/data/news/111383/,http://firrma.ru/data/news/123897/,http://firrma.ru/data/news/103216/,http://firrma.ru/data/news/104259/,http://firrma.ru/data/news/103984/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104434/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104424/,http://firrma.ru/data/news/104579/,http://firrma.ru/data/news/105173/,http://firrma.ru/data/news/105173/,http://firrma.ru/data/news/105169/,http://firrma.ru/data/news/103083/,http://firrma.ru/data/news/105199/,http://firrma.ru/data/news/105425/,http://firrma.ru/data/news/105538/,http://firrma.ru/data/news/105547/,http://firrma.ru/data/news/105551/,http://firrma.ru/data/news/105670/,http://firrma.ru/data/news/105667/,http://firrma.ru/data/news/106184/,http://firrma.ru/data/news/106202/,http://firrma.ru/data/news/106416/,http://firrma.ru/data/news/106475/,http://firrma.ru/data/news/106495/,http://firrma.ru/data/news/106505/,http://firrma.ru/data/news/107027/,http://firrma.ru/data/news/107289/"
tmp_data = tmp_str.split(",")
tmp_data = list(set(tmp_data))
print(len(tmp_data))



LINKS = tmp_data#["http://firrma.ru/data/news/107289/", "http://firrma.ru/data/news/106495/", "http://firrma.ru/data/news/106184/", "http://firrma.ru/data/news/107027/"]
words = []
similar = []
real_texts = []
for ent in LINKS:
    cur_text, cur_words, cur_similar = init(ent)
    words.append(cur_words)
    similar.append(cur_similar)
    real_texts.append(cur_text)


texts = [" ".join(ent) for ent in words]


def generate_model(obj):
  result_list = []
  for ent in obj:
    if len(ent[0]) > 1:
      tmp_list = [x[0].split("_")[0] for x in ent]
      result_list.append(tmp_list)
      #print(tmp_list)
  return result_list

#DOCUMENT_MODELS = []
INDEX_IN_USE = 2
documents_model = generate_model(similar[INDEX_IN_USE])

extractor = ner.Extractor()
for text in texts:
    for m in extractor(text):
        print(m, m.type)
    print()

len(documents_model)


def test(raw_documents, query_doc):
    from nltk.tokenize import word_tokenize
    gen_docs = raw_documents
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity(None, tf_idf[corpus],
                                          num_features=len(dictionary))
    sims_list = []
    maxes = []
    entities = []
    for ent in query_doc:
        query_doc_bow = dictionary.doc2bow(ent)
        query_doc_tf_idf = tf_idf[query_doc_bow]

    entities.append(ent)
    maxes.append(max(query_doc_tf_idf))
    sims_list.append(sims[query_doc_tf_idf])
    return entities, maxes, sims_list


def get_test_words(text):
    words = list(set(word_list(text)))
    entity = []
    for ent in words:
        if ent.isalpha():
            entity.append(ent + "_NOUN")
        else:
            entity.append(ent)
    similar = get_similar(entity)
    return text, words, similar


a_text, a_words, a_similar = get_test_words("Apple купил стартап Asaii, чтобы находить набирающих популярность музыкантов. Официально стоимость сделки не раскрывается, но источники предполагают, что она могла быть меньше $100 млн. Об этом рассказал Fortune. Сервис Asaii предоставляет аналитику лейблам и музыкальным агентам. Он предлагает им рекомендации и помогает найти перспективных артистов до того, как они станут всемирно известными. Apple собирается работать с молодыми исполнителями напрямую через Apple Music и заключать с ними эксклюзивные контракты. Ближайший конкурент Apple Music, музыкальный сервис Spotify, начал делать так год назад.")

b_entities, b_maxes, b_sims_list = test(documents_model, [a_words])
#entities, maxes, sims_list = test(documents_model, words)

print(a_words)
print(documents_model[np.argmax(b_sims_list)])
print()


tmp_str = ""
for index, value in enumerate(sims_list):
    try:
        tmp_str = tmp_str + str(index) + '\t\t\t' + str(round(maxes[index][1] * 100, 5)) + '%\t\t' + str(LINKS[index]) + '\t' + str(entities[index][:10]) + '\t' + '\n'
    except:
        tmp_str = tmp_str + str()
print('ЗА ОСНОВУ ДЛЯ СОЗДАНИЯ МОДЕЛИ ВЗЯТА СТАТЬЯ ' + LINKS[INDEX_IN_USE] + "\nКЛЮЧЕВЫЕ СЛОВА СТАТЬИ:" + str(words[INDEX_IN_USE]))
print('#\t    НА СКОЛЬКО СТАТЬЯ ПОХОЖА НА СДЕЛКУ\t\tССЫЛКА\t\t\t\t\tОСНОВНЫЕ СЛОВА ИЗ СТАТЬИ')
print()
print(tmp_str)


import numpy as np
tmp_sort_list = []
tmp_str = ""
for index, value in enumerate(sims_list):
    tmp_str = tmp_str + str(index) + '\t' + str(LINKS[index]) + "\t" + str(texts[index]) + "\n"
    tmp_sort_list.append(round(max(value), 5))
print('#\tССЫЛКА \t\t\t\t\tСЛОВА ИЗ СТАТЬИ')
print(tmp_str)
