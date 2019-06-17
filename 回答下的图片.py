from selenium import webdriver
import time
import json
import re
import os
import urllib.request
from lxml import etree
def GetCookies():
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        browser.add_cookie(cookie)
    browser.get('https://www.zhihu.com')
def GetImgs (Id, offsetlimit):
    aid = 400
    AllImg = set()
    while aid < offsetlimit:
        browser.get(('https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.content,voteup_count,created_time&offset={1}&limit=20&sort_by=default').format(Id,aid)
                    )
        pagecode = browser.page_source
        # print(pagecode)
        data = re.findall(r'{.*}', pagecode)[0]
        data = json.loads(data)
        for od in data['data']:
            testh = etree.HTML(od['content'])
            imgurls = testh.xpath("//img/@data-original")
            for imgurl in imgurls:
                # print(imgurl)
                if imgurl not in AllImg:
                    AllImg.add(imgurl)
                    Temp = '\n'.join(AllImg)
                    with open ('./temp.txt','w') as fi:
                        fi.write(Temp)
        aid += 20
        time.sleep(3)
    SaveImgs(AllImg, Id)
def SaveImgs(AllImg, Id):
    print('准备将ID为:%s的评论图片保存到本地...'% Id)
    patch = os.getcwd() + '/' + str(Id)
    if not os.path.exists(patch):
        os.makedirs(patch)
    for img in AllImg:
        filename = str(patch) + '/' + str(time.time()) + '.jpg'
        urllib.request.urlretrieve(img, filename=filename)
    print('本次采集共--' + str(len(AllImg)) + '--张图片')

if __name__ == '__main__':
    Id = '22212644'
    offsetlimit = 800
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    browser.get('https://www.zhihu.com')
    browser.delete_all_cookies()
    GetCookies()
    GetImgs(Id, offsetlimit)
