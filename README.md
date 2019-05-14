# VShaurme

Каркас для социальной сети «ВШаурме»

## Как установить локально

### Скачать исходный код

Сделать это можно тремя путями:

- командой `$ git clone https://github.com/devmanorg/vshaurme`
- с помощью [Github Desktop](https://desktop.github.com)
- скачать zip-архивом с помощью кнопки «Download as Zip»

![](https://user-images.githubusercontent.com/13587415/57612409-77a25580-757d-11e9-8550-45823e478067.png)

### Скачать зависимости

Убедитесь, что вы находитесь в папке с проектом:

```
$ cd vshaurme
```

и установите зависимости:

```
$ pip install -r requirements.txt
```

### Запустить

Дело за малым: наполнить сайт фейковыми данными и запустить:

```
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```

Сайт будет доступен по адресу `http://127.0.0.1:5000/`.


## Как запустить на Repl.it

1. Зарегистрироваться на [Repl.it](https://repl.it)
2. Создать новый repl, импортировать репозиторий [https://github.com/devmanorg/vshaurme](https://github.com/devmanorg/vshaurme)

    ![](https://user-images.githubusercontent.com/13587415/57639674-2021db00-75b9-11e9-9ca8-6dafefca9ce2.png)

3. Нажать «Run»

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке [Devman](http://dvmn.org).
