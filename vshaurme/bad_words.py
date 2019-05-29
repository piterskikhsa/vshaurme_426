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
        bad_words = [k for k, v in data.items() if v > 1 and len(k.split()) < 2]
        return bad_words


def get_ru_bad_words():
    url = "https://raw.githubusercontent.com/PixxxeL/djantimat/master/djantimat/fixtures/initial_data.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        bad_words = [word['fields']['word'] for word in data if len(word['fields']['word'].split()) < 2]
        trans_bad_words = list(map(lambda p: translit(p, reversed=True), bad_words))
        trans_bad_words_filetered = set(word.split("'")[0] for word in trans_bad_words)
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
    print(int(len(bad_words["en_bad_words"])), int(len(bad_words["ru_bad_words"])))

