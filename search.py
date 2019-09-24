import requests
import json
import time
import random
import pandas
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymongo


#链接数据库
client = pymongo.MongoClient('localhost', 27017) #链接数据库
youtube = client['youtube_keyword'] #建立数据库名称
table_name = youtube['get_video_url'] #表名

# 去除多余字符
def deal_control_char(s):
    temp=re.sub('[\\|*|/|:|?|"|<|>||]', '', s)
    return temp

# 获取60个视频链接
def detail(url):
    totail_list = []
    driver.get(url)
    time.sleep(1)
    # 滚动页面
    js = 'var action=document.documentElement.scrollTop=2000'
    driver.execute_script(js)
    time.sleep(1)
    js = 'var action=document.documentElement.scrollTop=4000'
    driver.execute_script(js)
    time.sleep(1)
    js = 'var action=document.documentElement.scrollTop=6000'
    driver.execute_script(js)
    time.sleep(1)
    js = 'var action=document.documentElement.scrollTop=8000'
    driver.execute_script(js)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    a = soup.select('#dismissable')

    for i in a:
        result = {}
        title = i.select('#video-title')[0].text.replace('\n', '').strip()
        container = i.select('#text-container')[0].text.replace('\n', '')
        if i.select('.style-scope .ytd-thumbnail-overlay-time-status-renderer'):
            times = i.select('.style-scope .ytd-thumbnail-overlay-time-status-renderer')[0].text.replace('\n', '').strip()
            if '兒歌' not in container and '儿歌' not in container and \
            '新聞' not in container and '新闻' not in container:
                result['times'] = i.select('.style-scope .ytd-thumbnail-overlay-time-status-renderer')[0].text.replace('\n', '').strip()
                result['container'] = i.select('#text-container')[0].text.replace('\n', '')
                result['title'] = title
                result['title_set'] = deal_control_char(title)
                result['href'] = 'https://www.youtube.com' + i.select('#video-title')[0].get('href')
                totail_list.append(result)
    return totail_list

def total(keyword, nums):
    url = 'https://www.youtube.com/results?search_query={}&sp=CAMSAhgB'.format(keyword)
    
    result = {}
    result['keyword'] = keyword
    result['down_nums'] = nums
    result['url'] = url
    result['details'] = detail(url)

    return result


if __name__ == '__main__':

    a = '西餐'
    down_nums = 40
    
    for key in a.split(' '):
        driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

        i = total('{}'.format(key), down_nums)

        print(i)

        # print(len(i[0]))

        with open('data.json', 'w') as f:
            json.dump(i, f)

        # # 保存表
        # table_name.insert_one(i)
        # # time.sleep(2)

        # # driver.quit()