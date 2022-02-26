import requests
from lxml import etree

if __name__ == '__main__':
    print('start')
    root = etree.XML(requests.get('https://sukebei.nyaa.si?page=rss').text)
    for channel in root.iterchildren('channel'):
        for item in channel.iterchildren('item'):
            title = item.xpath('title')[0].text
            url = item.xpath('guid')[0].text
            print(title)
            print(url)
            print()
    print('end')
