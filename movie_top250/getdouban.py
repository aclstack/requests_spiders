# -*- coding: utf-8 -*-
import requests
import re
from scrapy.selector import Selector
import MySQLdb

conn= MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='articlespider',
    charset='utf8',
    use_unicode=True)
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

def get_all_urls():
    for i in range(10):
        top_url = "https://movie.douban.com/top250?start={0}&filter=".format(i*25)

        response = requests.get(top_url, headers=headers)
        selector = Selector(text=response.text)
        #获取当前页的所有title的url
        all_title_urls = selector.css(".grid_view li .hd a::attr(href)").extract()
        for url in all_title_urls:
            try:
                response = requests.get(url, headers=headers)
                selector = Selector(text=response.text)
                top_number = selector.css('.top250 .top250-no ::text').extract()[0]
                match_obj = re.match(".*No\.(\d+).*", top_number)
                if match_obj:
                    top_number = match_obj.group(1)

                movie_name = selector.css('#content h1 span::text').extract()[0]
                print(top_number + "-- "+movie_name)
                direct_name = selector.css('#info .attrs a::text').extract()[0]
                score = selector.css('#interest_sectl .ll.rating_num::text').extract()[0]
                description = selector.css('#link-report span[property=v\:summary]::text').extract()[0]

                insert_sql = """
                    insert into movietop(url,top_number,movie_name,direct_name,score,description)
                    values(%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(insert_sql,(url,top_number,movie_name,direct_name,score,description))
                conn.commit()
            except Exception as e:
                continue



get_all_urls()

# top_number = ['No.1']
#
# match_obj = re.match(".*No\.(\d+).*", top_number)
# print(match_obj.group(1))