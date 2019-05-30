import json
import os
import requests

from transliterate import translit
from flask import current_app


def get_en_bad_words():
    url = "https://raw.githubusercontent.com/words/cuss/master/index.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        bad_words = []
        for word, rating in data.items():
            if rating > 1 and len(word.split()) < 2 and len(word) > 2:
                bad_words.append(word)
        return bad_words


def get_ru_bad_words():
    url = "https://raw.githubusercontent.com/PixxxeL/djantimat/master/djantimat/fixtures/initial_data.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        bad_words = []
        for result in data:
            bad_word = result['fields']['word']
            if len(bad_word.split()) < 2:       # отбрасываем фразы, нас интересуют только слова
                bad_words.append(bad_word)

        # Конвертируем с русского языка в транслит:
        trans_bad_words = list(map(lambda p: translit(p, reversed=True), bad_words))

        # Отфильтровываем некоторые словоформы и короткие слова:
        trans_bad_words_filetered = set()
        for word in trans_bad_words:
            word_form = word.split("'")[0]
            if len(word_form) > 2:
                trans_bad_words_filetered.add(word_form)

        return list(trans_bad_words_filetered)


def write_to_file(data):
    badwords_dir = current_app.config['VSHAURME_BADWORDS_PATH']
    for name, words in data.items():
        with open(os.path.join(badwords_dir, f"{name}.json"), "w") as f:
            f.write(json.dumps({"words": words}))


def init_badwords_files():
    bad_words = {
        "en_bad_words": get_en_bad_words(),
        "ru_bad_words": get_ru_bad_words()
    }
    write_to_file(bad_words)
    en_bad_words_num = len(bad_words["en_bad_words"])
    ru_bad_words_num = len(bad_words["ru_bad_words"])
    message = f'''
    en_bad_words: {en_bad_words_num}
    ru_bad_words: {ru_bad_words_num}
    Total: {sum([en_bad_words_num, ru_bad_words_num])}
    '''
    return message
