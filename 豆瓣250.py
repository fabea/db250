import re
import pandas as pd
import requests
from lxml import etree

df = pd.DataFrame()

headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
}

url_lists = [
    "https://movie.douban.com/top250?start=" + str(i * 25) for i in range(10)
]


def get_info(url):
    global df
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    movies = html.xpath("//div[@class='item']")
    placeholders = ['-', '-', '-']
    for movie in movies:
        titles = movie.xpath(
            "./div[@class='info']/div[@class='hd']/a/span/text()")
        movie_titles = []
        for title in titles:
            title = re.sub(r"/(\w+)", r'\1', title.replace('\xa0', ''))
            movie_titles.append(title)
        movie_titles = movie_titles + placeholders[len(movie_titles):]
        rating = movie.xpath(
            "./div[@class='info']//span[@class='rating_num']/text()")[0]
        series = pd.Series({
            '中文电影名': movie_titles[0],
            '英文电影名': movie_titles[1],
            '其他电影名': movie_titles[2],
            '评分': rating
        })
        df = df.append(series, ignore_index=True)


for url in url_lists:
    get_info(url)

print(df)

df.to_csv('douban250.csv', index=False, encoding='utf-8')
