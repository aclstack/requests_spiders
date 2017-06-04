# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
import time
import random
import threading
from urllib import parse

#定义user-agent代理
user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

# 博客列表
blog_url_list = [
    'http://blog.csdn.net/mockingbirds/article/details/50663327',
    'http://blog.csdn.net/mockingbirds/article/details/72854243',
    'http://blog.csdn.net/mockingbirds/article/details/72850237',
    'http://blog.csdn.net/mockingbirds/article/details/72808709',
    'http://blog.csdn.net/mockingbirds/article/details/72794611',
    'http://blog.csdn.net/mockingbirds/article/details/72078407',
    'http://blog.csdn.net/mockingbirds/article/details/71809358',
    'http://blog.csdn.net/mockingbirds/article/details/71022785',
    'http://blog.csdn.net/mockingbirds/article/details/68957146',
    'http://blog.csdn.net/mockingbirds/article/details/68951014',
    'http://blog.csdn.net/mockingbirds/article/details/65930764',
    'http://blog.csdn.net/mockingbirds/article/details/64950241',
    'http://blog.csdn.net/mockingbirds/article/details/64501329',
    'http://blog.csdn.net/mockingbirds/article/details/59641983',
    'http://blog.csdn.net/mockingbirds/article/details/58670450',
    'http://blog.csdn.net/mockingbirds/article/details/58663262',
    'http://blog.csdn.net/mockingbirds/article/details/58283188',
    'http://blog.csdn.net/mockingbirds/article/details/54743179',
    'http://blog.csdn.net/mockingbirds/article/details/54671588',
    'http://blog.csdn.net/mockingbirds/article/details/54565224',
    'http://blog.csdn.net/mockingbirds/article/details/54429663',
    'http://blog.csdn.net/mockingbirds/article/details/54382072',
    'http://blog.csdn.net/mockingbirds/article/details/54293099',
    'http://blog.csdn.net/mockingbirds/article/details/53998292',
    'http://blog.csdn.net/mockingbirds/article/details/53976259',
    'http://blog.csdn.net/mockingbirds/article/details/53946575',
    'http://blog.csdn.net/mockingbirds/article/details/53700187',
    'http://blog.csdn.net/mockingbirds/article/details/53494192',
    'http://blog.csdn.net/mockingbirds/article/details/53453790',
    'http://blog.csdn.net/mockingbirds/article/details/53453326',
    'http://blog.csdn.net/mockingbirds/article/details/53367474',
    'http://blog.csdn.net/mockingbirds/article/details/53292126',
    'http://blog.csdn.net/mockingbirds/article/details/53242610',
    'http://blog.csdn.net/mockingbirds/article/details/53239309',
    'http://blog.csdn.net/mockingbirds/article/details/53239265',
    'http://blog.csdn.net/mockingbirds/article/details/53178579',
    'http://blog.csdn.net/mockingbirds/article/details/53164773',
    'http://blog.csdn.net/mockingbirds/article/details/53152426',
    'http://blog.csdn.net/mockingbirds/article/details/53143626',
    'http://blog.csdn.net/mockingbirds/article/details/53134429',
    'http://blog.csdn.net/mockingbirds/article/details/53134076',
    'http://blog.csdn.net/mockingbirds/article/details/53087402',
    'http://blog.csdn.net/mockingbirds/article/details/53048296',
    'http://blog.csdn.net/mockingbirds/article/details/53048209',
    'http://blog.csdn.net/mockingbirds/article/details/53039691',
    'http://blog.csdn.net/mockingbirds/article/details/53026770',
    'http://blog.csdn.net/mockingbirds/article/details/52742757',
    'http://blog.csdn.net/mockingbirds/article/details/52738552',
    'http://blog.csdn.net/mockingbirds/article/details/52738368',
    'http://blog.csdn.net/mockingbirds/article/details/52728487',
    'http://blog.csdn.net/mockingbirds/article/details/52727251',
    'http://blog.csdn.net/mockingbirds/article/details/52722965',
    'http://blog.csdn.net/mockingbirds/article/details/52012696',
    'http://blog.csdn.net/mockingbirds/article/details/51930536',
    'http://blog.csdn.net/mockingbirds/article/details/51878431',
    'http://blog.csdn.net/mockingbirds/article/details/51336105',
    'http://blog.csdn.net/mockingbirds/article/details/51334924',
    'http://blog.csdn.net/mockingbirds/article/details/51289416',
    'http://blog.csdn.net/mockingbirds/article/details/51166173',
    'http://blog.csdn.net/mockingbirds/article/details/50923234',
    'http://blog.csdn.net/mockingbirds/article/details/50885768',
    'http://blog.csdn.net/mockingbirds/article/details/50878920',
    'http://blog.csdn.net/mockingbirds/article/details/50830137',
    'http://blog.csdn.net/mockingbirds/article/details/50821998',
    'http://blog.csdn.net/mockingbirds/article/details/50733262',
    'http://blog.csdn.net/mockingbirds/article/details/50718604',
    'http://blog.csdn.net/mockingbirds/article/details/50708107',
    'http://blog.csdn.net/mockingbirds/article/details/50707465',
    'http://blog.csdn.net/mockingbirds/article/details/50700552',
    'http://blog.csdn.net/mockingbirds/article/details/50663327',
    'http://blog.csdn.net/mockingbirds/article/details/50658846',
    'http://blog.csdn.net/mockingbirds/article/details/50649717',
    'http://blog.csdn.net/mockingbirds/article/details/50644940',
    'http://blog.csdn.net/mockingbirds/article/details/50642817',
    'http://blog.csdn.net/mockingbirds/article/details/50639861',
    'http://blog.csdn.net/mockingbirds/article/details/50615686',
    'http://blog.csdn.net/mockingbirds/article/details/50550689',
    'http://blog.csdn.net/mockingbirds/article/details/50539282',
    'http://blog.csdn.net/mockingbirds/article/details/50536001',
    'http://blog.csdn.net/mockingbirds/article/details/50533449',
    'http://blog.csdn.net/mockingbirds/article/details/50532855',
    'http://blog.csdn.net/mockingbirds/article/details/50489120',
    'http://blog.csdn.net/mockingbirds/article/details/50485271',
    'http://blog.csdn.net/mockingbirds/article/details/50465294',
    'http://blog.csdn.net/mockingbirds/article/details/50459143',
    'http://blog.csdn.net/mockingbirds/article/details/50452370',
    'http://blog.csdn.net/mockingbirds/article/details/47706779',
    'http://blog.csdn.net/mockingbirds/article/details/49804703',
    'http://blog.csdn.net/mockingbirds/article/details/49642839',
    'http://blog.csdn.net/mockingbirds/article/details/49517523',
    'http://blog.csdn.net/mockingbirds/article/details/49497451',
    'http://blog.csdn.net/mockingbirds/article/details/49456517',
    'http://blog.csdn.net/mockingbirds/article/details/49455421',
    'http://blog.csdn.net/mockingbirds/article/details/49454987',
    'http://blog.csdn.net/mockingbirds/article/details/49454279',
    'http://blog.csdn.net/mockingbirds/article/details/48844807',
    'http://blog.csdn.net/mockingbirds/article/details/48844603',
    'http://blog.csdn.net/mockingbirds/article/details/48749375',
    'http://blog.csdn.net/mockingbirds/article/details/48594969',
    'http://blog.csdn.net/mockingbirds/article/details/48572225',
    'http://blog.csdn.net/mockingbirds/article/details/48412967',
    'http://blog.csdn.net/mockingbirds/article/details/48419319',
    'http://blog.csdn.net/mockingbirds/article/details/48103361',
    'http://blog.csdn.net/mockingbirds/article/details/47859117',
    'http://blog.csdn.net/mockingbirds/article/details/47856695',
    'http://blog.csdn.net/mockingbirds/article/details/47701635',
    'http://blog.csdn.net/mockingbirds/article/details/47376939',
    'http://blog.csdn.net/mockingbirds/article/details/47374127',
    'http://blog.csdn.net/mockingbirds/article/details/47344955',
    'http://blog.csdn.net/mockingbirds/article/details/47324089',
    'http://blog.csdn.net/mockingbirds/article/details/47302815',
    'http://blog.csdn.net/mockingbirds/article/details/47058555',
    'http://blog.csdn.net/mockingbirds/article/details/47053483',
    'http://blog.csdn.net/mockingbirds/article/details/46958877',
    'http://blog.csdn.net/mockingbirds/article/details/46942667',
    'http://blog.csdn.net/mockingbirds/article/details/46845273',
    'http://blog.csdn.net/mockingbirds/article/details/46843295',
    'http://blog.csdn.net/mockingbirds/article/details/46842327',
    'http://blog.csdn.net/mockingbirds/article/details/46685559',
    'http://blog.csdn.net/mockingbirds/article/details/46673447',
    'http://blog.csdn.net/mockingbirds/article/details/46671509',
    'http://blog.csdn.net/mockingbirds/article/details/46669433',
    'http://blog.csdn.net/mockingbirds/article/details/46662579',
    'http://blog.csdn.net/mockingbirds/article/details/46626755',
    'http://blog.csdn.net/mockingbirds/article/details/46611523',
    'http://blog.csdn.net/mockingbirds/article/details/46594107',
    'http://blog.csdn.net/mockingbirds/article/details/46584473',
    'http://blog.csdn.net/mockingbirds/article/details/46573221',
    'http://blog.csdn.net/mockingbirds/article/details/46572919',
    'http://blog.csdn.net/mockingbirds/article/details/46571909',
    'http://blog.csdn.net/mockingbirds/article/details/46508465',
    'http://blog.csdn.net/mockingbirds/article/details/46489725',
    'http://blog.csdn.net/mockingbirds/article/details/46489163',
    'http://blog.csdn.net/mockingbirds/article/details/46462149',
    'http://blog.csdn.net/mockingbirds/article/details/46419693',
    'http://blog.csdn.net/mockingbirds/article/details/46418845',
    'http://blog.csdn.net/mockingbirds/article/details/46402441',
    'http://blog.csdn.net/mockingbirds/article/details/46054419',
    'http://blog.csdn.net/mockingbirds/article/details/45953689',
    'http://blog.csdn.net/mockingbirds/article/details/45936831',
    'http://blog.csdn.net/mockingbirds/article/details/45935909',
    'http://blog.csdn.net/mockingbirds/article/details/45935069',
    'http://blog.csdn.net/mockingbirds/article/details/45924207',
    'http://blog.csdn.net/mockingbirds/article/details/45897615',
    'http://blog.csdn.net/mockingbirds/article/details/45854007',
    'http://blog.csdn.net/mockingbirds/article/details/45849523',
    'http://blog.csdn.net/mockingbirds/article/details/45832217',
    'http://blog.csdn.net/mockingbirds/article/details/45487035',
    'http://blog.csdn.net/mockingbirds/article/details/45460143',
    'http://blog.csdn.net/mockingbirds/article/details/45444793',
    'http://blog.csdn.net/mockingbirds/article/details/45441337',
    'http://blog.csdn.net/mockingbirds/article/details/45440683',
    'http://blog.csdn.net/mockingbirds/article/details/45421861',
    'http://blog.csdn.net/mockingbirds/article/details/45399691',
    'http://blog.csdn.net/mockingbirds/article/details/45372523',
    'http://blog.csdn.net/mockingbirds/article/details/45341655',
    'http://blog.csdn.net/mockingbirds/article/details/45291041',
    'http://blog.csdn.net/mockingbirds/article/details/45290659',
    'http://blog.csdn.net/mockingbirds/article/details/45290105',
    'http://blog.csdn.net/mockingbirds/article/details/45287127',
    'http://blog.csdn.net/mockingbirds/article/details/45271917',
    'http://blog.csdn.net/mockingbirds/article/details/45252003',
    'http://blog.csdn.net/mockingbirds/article/details/45225833',
    'http://blog.csdn.net/mockingbirds/article/details/45157431',
    'http://blog.csdn.net/mockingbirds/article/details/45156407',
    'http://blog.csdn.net/mockingbirds/article/details/45132551',
    'http://blog.csdn.net/mockingbirds/article/details/45131455',
    'http://blog.csdn.net/mockingbirds/article/details/45116967',
    'http://blog.csdn.net/mockingbirds/article/details/44945865',
    'http://blog.csdn.net/mockingbirds/article/details/44945309',
    'http://blog.csdn.net/mockingbirds/article/details/44945251',
    'http://blog.csdn.net/mockingbirds/article/details/44903155',
    'http://blog.csdn.net/mockingbirds/article/details/44902965',
    'http://blog.csdn.net/mockingbirds/article/details/44902705',
    'http://blog.csdn.net/mockingbirds/article/details/44889323',
    'http://blog.csdn.net/mockingbirds/article/details/44859041',
    'http://blog.csdn.net/mockingbirds/article/details/44840071',
    'http://blog.csdn.net/mockingbirds/article/details/44839305',
    'http://blog.csdn.net/mockingbirds/article/details/44838729',
    'http://blog.csdn.net/mockingbirds/article/details/44838613',
    'http://blog.csdn.net/mockingbirds/article/details/44838215',
    'http://blog.csdn.net/mockingbirds/article/details/44837935',
    'http://blog.csdn.net/mockingbirds/article/details/44814613',
    'http://blog.csdn.net/mockingbirds/article/details/44814357',
    'http://blog.csdn.net/mockingbirds/article/details/44813529',
    'http://blog.csdn.net/mockingbirds/article/details/44812565',
    'http://blog.csdn.net/mockingbirds/article/details/44812401',
    'http://blog.csdn.net/mockingbirds/article/details/44812031',
    'http://blog.csdn.net/mockingbirds/article/details/44811889',
    'http://blog.csdn.net/mockingbirds/article/details/44788111',
    'http://blog.csdn.net/mockingbirds/article/details/44785705',
    'http://blog.csdn.net/mockingbirds/article/details/44785289',
    'http://blog.csdn.net/mockingbirds/article/details/44181045',
    'http://blog.csdn.net/mockingbirds/article/details/43374223',
    'http://blog.csdn.net/mockingbirds/article/details/43201681',
    'http://blog.csdn.net/mockingbirds/article/details/43166663',
    'http://blog.csdn.net/mockingbirds/article/details/43166265',
    'http://blog.csdn.net/mockingbirds/article/details/43164037',
    'http://blog.csdn.net/mockingbirds/article/details/43163639',
    'http://blog.csdn.net/mockingbirds/article/details/42609843',
    'http://blog.csdn.net/mockingbirds/article/details/42609671',
    'http://blog.csdn.net/mockingbirds/article/details/42245991',
    'http://blog.csdn.net/mockingbirds/article/details/42245841',
    'http://blog.csdn.net/mockingbirds/article/details/41732325',
    'http://blog.csdn.net/mockingbirds/article/details/41731327',
    'http://blog.csdn.net/mockingbirds/article/details/41596299',
    'http://blog.csdn.net/mockingbirds/article/details/41365525',
    'http://blog.csdn.net/mockingbirds/article/details/41364251',
    'http://blog.csdn.net/mockingbirds/article/details/41358499',
    'http://blog.csdn.net/mockingbirds/article/details/41297911',
    'http://blog.csdn.net/mockingbirds/article/details/41296727',
    'http://blog.csdn.net/mockingbirds/article/details/41293793',
    'http://blog.csdn.net/mockingbirds/article/details/41262539',
    'http://blog.csdn.net/mockingbirds/article/details/41258493',
    'http://blog.csdn.net/mockingbirds/article/details/41129307',
    'http://blog.csdn.net/mockingbirds/article/details/41128925',
    'http://blog.csdn.net/mockingbirds/article/details/41053317',
    'http://blog.csdn.net/mockingbirds/article/details/41053121',
    'http://blog.csdn.net/mockingbirds/article/details/41052051',
    'http://blog.csdn.net/mockingbirds/article/details/41019919',
    'http://blog.csdn.net/mockingbirds/article/details/41018925',
    'http://blog.csdn.net/mockingbirds/article/details/40924043',
    'http://blog.csdn.net/mockingbirds/article/details/40923961',
    'http://blog.csdn.net/mockingbirds/article/details/40794865',
    'http://blog.csdn.net/mockingbirds/article/details/40713867',
    'http://blog.csdn.net/mockingbirds/article/details/40682679',

]

class IncreateReadCount(object):

    # 获取当前博客的所有url列表
    def get_blog_urls(self):
        for i in range(1, 16):
            url = "http://blog.csdn.net/mockingbirds/article/list/{0}".format(i)
            headers = {
                'User-Agent':random.choice(user_agent_list)
            }
            response = requests.get(url, headers=headers)
            selector = Selector(text=response.text)
            url = selector.css('.list_item_new span[class="link_title"] a::attr(href)').extract()
            for j in range(len(url)):
                url_j = url[j]
                url_title = parse.urljoin("http://blog.csdn.net",url_j)
                print("'"+url_title+"',")
                blog_url_list.append(url_title)

    # 随机访问blog_url_list中的url
    def spider_read(self):
        for i in range(1000):
            try:
                url = random.choice(blog_url_list) #从blog_url_list列表中随机抽取一个url访问
                headers = {
                    'User-Agent': random.choice(user_agent_list) #随机设置user-agent
                }
                response = requests.get(url, headers=headers)
                selector = Selector(text=response.text)
                view = selector.css('.article_r .link_view::text').extract()[0] #当前url的访问次数
                title = selector.css('#article_details .link_title a::text').extract()[0] # 当前url对应的标题
                visit_count = selector.css('#blog_rank li span::text').extract()[0]  #当前用户总的访问次数
                print(view +"  浏览次数："+visit_count+ "    i is :" + str(i)+"   title is :"+title)
                time.sleep(random.randint(3, 5))
                if i == 15:
                    time.sleep(12)
            except:
                time.sleep(10)
                continue

class MyThread(threading.Thread):
    def __init__(self,arg):
        super(MyThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.arg=arg

    def run(self):#定义每个线程要运行的函数
        increate_count = IncreateReadCount()
        increate_count.spider_read()

# increate_count = IncreateReadCount()
# increate_count.spider_read()

for i in range(300):
    blog_thread = MyThread(i)
    blog_thread.start()


