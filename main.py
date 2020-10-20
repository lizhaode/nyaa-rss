import os

import pymysql
import requests
from lxml import etree


class MySQL:
    def __init__(self):
        print(os.getenv('host'))
        print(os.getenv('port'))
        self._connect = pymysql.Connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'),
                                        database=os.getenv('database'), port=int(os.getenv('port')), autocommit=True)
        self._cursor = self._connect.cursor()

    def save(self, title: str, url: str) -> None:
        sql_sentence = 'INSERT INTO fetch_rss (title, guid) VALUES (%s, %s)'
        self._cursor.execute(sql_sentence, (title, url))

    def close(self) -> None:
        self._cursor.close()
        self._connect.close()


if __name__ == '__main__':
    print('start')
    sql = MySQL()
    root = etree.XML(requests.get('https://sukebei.nyaa.si?page=rss').text)
    for channel in root.iterchildren('channel'):
        for item in channel.iterchildren('item'):
            title = item.xpath('title')[0].text
            url = item.xpath('guid')[0].text
            sql.save(title, url)
    sql.close()
    print('end')
