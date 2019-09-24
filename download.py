import os
import time
import random
import json

import youtube_dl

def channel(key):
    channel_list = []
    with open('{}.json'.format(key), 'r') as f:
        data = json.load(f)
        channel_list.append(data)
    return channel_list

def download(url, folder, title):

    video_info = youtube_dl.YoutubeDL().extract_info(url, download=False)
    formats = video_info.get('formats')
    format_list = []
    for i in formats:
        a = i.get('format').split(' - ')[0]
        format_list.append(a)

    ydl_opts = {
        'outtmpl': '/root/{}/{}'.format(folder, title)
    }
    
    # 检测480p分辨率，如果没有就用默认的。
    if '135' in format_list:
        ydl_opts['format'] = '135+m4a'
    else:
        ydl_opts['format'] = 'mp4+m4a'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)

if __name__ == '__main__':

    a = 'vlog 动画 日本医疗'

    for key in a.split(' '):
        channel_list = channel(key)

        for i in channel_list:

            keyword = i['keyword']
            down_nums = i['down_nums']
            details_list = i['details']

            # 创建目录
            file_path = os.path.exists('/root/{}'.format(keyword))
            if not file_path:
                os.mkdir('/root/{}'.format(keyword))
                print('{}'.format(keyword)+'目录创建成功')

            else:
                print('{}'.format(keyword)+'目录已存在')

            # 下载失败记录
            failure_list = []

            # 开始下载
            for video in details_list:
                title_set = video['title_set']
                title_set_mp4 = title_set + '.mp4'
                href = video['href']

                mp4_list = []
                for root,dirs,files in os.walk('/root/{}'.format(keyword)):
                    
                    for mp4 in files:
                        if '.mp4' in mp4:
                            mp4_list.append(mp4)

                # 已经下过的视屏，包含失败的
                down_video_list = mp4_list + failure_list


                if len(mp4_list)<down_nums:
                    if title_set_mp4 not in down_video_list:
                        try:
                            download(href, keyword, title_set)
                            print(details_list.index(video)+1)
                        except:
                            # 保存表
                            failure_list.append(title_set_mp4)
                            print('{}下载失败'.format(details_list.index(video)+1))
                       
                            time.sleep(random.randint(1, 3))  # 限制爬取时间
