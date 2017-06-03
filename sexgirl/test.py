# -*- coding: utf-8 -*-

dict_test = {
    '111':111,
    '222':222,
    '333':333,
}

# keys = dict_test.keys()
# for key in keys:
#     print("key is :"+key+"   value is :"+str(dict_test.get(key)))
#
# title = ['aaa','bbb','ccc']
#
# for i in range(3):
#     print(title[i])

# import re
# str = '<span>64</span>'
# match_obj = re.match("<span>(\d+)</span>",str)
# if match_obj:
#     print(match_obj.group(1))
# else:
#     print('nothing match')

import re
# origin = 'http://i.meizitu.net/2017/04/24b01.jpg'
# print(origin[-9:-4])
# match_obj = re.match('.*/(.*).jpg', origin) #解析出当前的图片后缀名,用于后面的替换
# next_image_url = ""
# if match_obj:
#     match_result = match_obj.group(1)
#     page_number = 45
#     for i in range(1,46):
#         if i < 10:
#             next_image_url = match_result.replace(match_result[-2:], "0"+str(i), 1)
#         else:
#             next_image_url = match_result.replace(match_result[-2:], str(i), 1)
#
#         next_image_url = origin.replace(match_result, next_image_url,1)
#         print(next_image_url)


# import os
# base_dir = "/home/liuhang/code/sexgirl/{0}".format("abc")
# if os.path.exists(base_dir):
#     print('false')
# else:
#     print('true')

import urllib
# import requests
# print('Downloading...')
# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
# }
# img_response = requests.get("http://i.meizitu.net/2017/04/24b01.jpg", headers=headers)
# f = open('/home/liuhang/code/sexgirl/abc/a.jpg', 'ab')
# f.write(img_response.content) #多媒体文件要是用conctent
# f.close()



# for i in range(64):
#     str = origin.


pages_nav = ['<span>«上一组</span>', '<span>2</span>', '<span>3</span>', '<span>4</span>', '<span>47</span>', '<span>下一页»</span>']
total_page = pages_nav[len(pages_nav)-2]
match_obj = re.match("<span>(\d+)</span>", total_page)
if match_obj:
    total_page = match_obj.group(1)
    print(total_page)