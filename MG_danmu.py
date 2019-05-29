import requests
import pandas as pd
import time
import datetime
from fake_useragent import UserAgent

ua = UserAgent()
url = "https://galaxy.bz.mgtv.com/rdbarrage"

rdb_content = {'id': [], 'type': [], 'uid': [], 'content': [], 'add_time': [], 'ups': []}
count = 0

print("爬取开始时间: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

for i in range(0, 91):

    querystring = {"version": "2.0.0", "vid": "5683459", "cid": "328724", "time": i*60000}

    headers = {
        'User-Agent': ua.random
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        items = response['data']['items']
        if items is None:
            print("爬取完毕！弹幕数量{}".format(count))
            break
        else:
            for item in items:
                rdb_content['id'].append(item.get('id')) #弹幕id
                rdb_content['type'].append(item.get('type')) #弹幕类型
                rdb_content['uid'].append(item.get('uid')) #用户id
                rdb_content['content'].append(item.get('content')) #弹幕内容
                rdb_content['add_time'].append(item.get('time')) #弹幕时间
                rdb_content['ups'].append(item.get('up', 0)) #d弹幕点赞数
                count = count + 1

            print("爬取第{}分钟的弹幕...，当前弹幕数量{}".format(i + 1, count))
        time.sleep(5)
    except:
        print("第{}分钟弹幕爬取失败!当前弹幕数量{}".format(i + 1, count))
        continue
    rdb_df = pd.DataFrame(rdb_content)
    rdb_df.to_csv('rdb.csv', index=None)
