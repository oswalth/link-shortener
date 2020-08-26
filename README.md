# LinkShortener

Тестовое задание - Написать ICQ/Telegram/TamTam бота на python, который умеет делать 2 вещи :
Есть вот такой сервис сокращения ссылок : https://rel.ink/
Первое: боту можно отправить ссылку, он вернет сокращенный вариант
Второе: у бота можно спросить 10 последних ссылок сделанных для меня.

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Создание БД для хранения укороченных ссылок

```bash
python setyp.py
```

## 3. Включение бота

```bash
python bot.py
```

# Информация о работе:

## 1. Ссылка должна быть полной - содержать протокол, доменное имя (опцианально - url, якорь)

## 2. Запрос 10 последних ссылок пользователя выводяться при нажатии на кнопку "/history", под формой ввода

## 3. При ошибке со стороны API бот выдаст сообщение - "Сервис временно недоступен. Попробуйте позже"

# API

[url shortener](https://rel.ink/)