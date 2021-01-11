import sqlite3
import time
import requests
import config
import json


def insert_link(chat_id, link, short_link): 
  with sqlite3.connect('messages.db') as db:
    sql = db.cursor()
    sql.execute(f"""SELECT shortened_link FROM ShortLink 
                    WHERE shortened_link=? AND chat_id=?""", (short_link, chat_id)
                    )
    if sql.fetchone() is None:
      print(f"Добавляем {link}")
      sql.execute(f"""INSERT INTO ShortLink (chat_id, link, shortened_link, sent_at) 
                      VALUES(?,?,?,?)""",
                      (str(chat_id), link, short_link, time.time())
                      )
      print('Запись сохранена в БД')
    else:
      sql.execute(f"""UPDATE ShortLink
                     SET sent_at=? 
                     WHERE chat_id=? AND link=?""", (time.time(), chat_id, link))
    db.commit()
    


def select_links(message):
  with sqlite3.connect('messages.db') as db:
    sql = db.cursor()
    sql.execute(f"""SELECT shortened_link FROM ShortLink
                    WHERE chat_id=? ORDER BY sent_at DESC LIMIT 10""", (message.chat.id,))

    latest_links = sql.fetchall()
    if latest_links:
      return "Последние 10 укороченных ссылок:\n" + "\n".join([row[0] for row in latest_links])
    return "История пуста. Отправьте ссылку"


def shorten_links(links, chat_id):
    request_headers = {
        "Content-type": "application/json",
        "apikey": config.API_KEY,
        "workspace": config.WORKSPACE_ID
    }
    short_links = []
    for link in links:
        link_request = {
            "destination": link,
            "domain": {"fullName": "rebrand.ly"}
        }
        http_response = requests.post(config.SHORTENER_LINK, json.dumps(link_request), headers=request_headers)
        # Если ссылка обработалась правильно
        if http_response.status_code == requests.codes.ok:
            link = http_response.json()
            short_link = link["shortUrl"]

          # Записываем результат сокращения ссылки в БД и добавляем к ответу бота
            insert_link(chat_id, link, short_link)
            short_links.append(f"{link} - {short_link}")

        # Если неправильный запрос
        elif str(http_response.status_code)[0] == '4':
            msg = f"Неверный адрес - {link}, попробуйте заново."
            short_links.append(msg)

        # Если лежит api
        elif str(http_response.status_code)[0] == '5':
            msg = "Сервис временно недоступен. Попробуйте позже\U0001F4A4"
            short_links.append(msg)
            break

        # Непредвиденные обстоятельства
        else:
            msg = "Ошибка"
            short_links.append(msg)
            break
    if short_links:
        return "\n".join([short_link for short_link in short_links])
    return "Текст не содержит ссылок типа https://site.com\U0001F614"
