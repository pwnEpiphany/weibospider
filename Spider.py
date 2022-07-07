import json
import requests
import urllib
import urllib.request
import urllib.parse
import os
from config import config
import threading
from bs4 import BeautifulSoup
import csv
import pandas as pd
# class MainThread(threading.Thread)
class myThread (threading.Thread):
    def __init__(self, threadID, index,name, idx,ids,mids):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ids = ids
        self.mids = mids
        self.idx = idx
        self.index = index
    def run(self):
        print ("开始线程：" + self.name)
        search_details(self.idx,self.ids,self.mids)
        print ("退出线程：" + self.name)


headers = {"Cookie": "_T_WM=63609169492; XSRF-TOKEN=dc15ea; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=oid%3D4774734652506260%26luicode%3D10000011%26lfid%3D102803",
 "host": "m.weibo.cn", "proxys": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
    
def get_json_from_url(url):
    html = requests.get(url, headers=headers).text
    datas = json.loads(html)
    return datas

def search_for_everyone(name):
    url1 = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%253D1%2526q%253D{}&page_type=searchall".format(urllib.parse.quote(name))
    print(url1)
    datas = get_json_from_url(url1) 
    ids = []
    mids = []
    for i in range(min(10,len(datas["data"]["cards"]))):
        roots = datas["data"]["cards"][i]
        keys = []
        for key in roots:
            keys.append(key)
        print(keys)
        if "mblog" in keys:
            ids.append(datas["data"]["cards"][i]["mblog"]["id"])
            mids.append(datas["data"]["cards"][i]["mblog"]["mid"])
        elif "card_group" in keys:
            rooots1 = datas["data"]["cards"][i]["card_group"]
            str1 = str(rooots1)
            try:
                kk = str1.index("'mid': ")
                kk1 = str1.index("'id': ")
                mids.append(str(str1[kk+8:kk+24]))
                ids.append(str(str1[kk1+7:kk1+23]))
            except:
                continue
        else:
            print("wrong")
            continue
    return ids,mids

    #json文件格式
    #name{
    #    id:
    #    mid:
    #    detail:
    #    comment:[0，1，2，3，4，5，6，7，8，9]   
    #}
def search_details(idx,ids,mids):
    detail_url = "https://m.weibo.cn/statuses/extend?id={}".format(ids)
    comment_url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(ids,mids)
    answer_json = {"id":ids,"mid":mids}
    details = get_json_from_url(detail_url)
    comment = get_json_from_url(comment_url)
    detail = details["data"]["longTextContent"]
    comments = []
    if comment["ok"] == 0:
        comments = []   
    else:
        max_len = len(comment["data"]["data"])
        if max_len >=10:
            for i in range(10):
                kk = {"name":comment["data"]["data"][i]["user"]["screen_name"],"text":comment["data"]["data"][i]["text"]}
                comments.append(kk)
        else:
            for i in range(max_len):
                kk = {"name":comment["data"]["data"][i]["user"]["screen_name"],"text":comment["data"]["data"][i]["text"]}
                comments.append(kk)
    answer_json["detail"] = detail
    answer_json["comment"] = comments
    datadict = json.dumps(answer_json)
    with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(idx+10),'w') as f:
        f.write(datadict)

def search_all_with_name(index,name):
    ids = []
    mids = []
    threads = []
    ids,mids = search_for_everyone(name)
    for i in range(len(ids)):
        threads.append(myThread(index,i,"Thread-{}".format(i),i,ids[i],mids[i]))
    for th in threads:
        th.start()
    for en in threads:
        en.join()
    print("search over")
    total_dict = {"name":name}
    content = []
    for i in range(len(ids)):
        with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(index),'w') as f1: 
            for i in range(len(ids)):
                with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(i+10),'r') as f:       
                    file = json.loads(f.read())
                    content.append(file)
            total_dict["content"] = content
            tmp = json.dumps(total_dict)
            f1.write(tmp)



class spider():
    def __init__(self, Cookie = "_T_WM=63609169492; XSRF-TOKEN=dc15ea; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=oid%3D4774734652506260%26luicode%3D10000011%26lfid%3D102803"):
        self.cookie = Cookie
        self.host = "m.weibo.cn"
        self.proxys = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"]
        self.headers = {"Cookie": self.cookie, "User-Agent": self.proxys[0]}
        configs = config()
        self.json_path = configs.json_path


    def clear_all(self,dir):
        if not os.path.exists(dir):
            return False
        if os.path.isfile(dir):
            os.remove(dir)
            return
        for i in os.listdir(dir):
            t = os.path.join(dir, i)
            if os.path.isdir(t):
                self.deldir(t)  # 重新调用次方法
            else:
                os.unlink(t)
        os.removedirs(dir)  # 递归删除目录下面的空文件夹

    def clear(self,name):
        target = name
        if (os.path.exists(target)):
            os.remove(target)


    def Hotsearch(self):  # return dict
        self.clear("/home/tamako/Desktop/allin/weibopy/static/datas/hot.csv")
        urls = "https://s.weibo.com/top/summary?cate=realtimehot"
        html = requests.get(urls, headers=self.headers).content
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('td', class_='td-02')
        # print(items)
        for i, item in enumerate(items[1:50]):
            result = []    
            rank = '第{0}名'.format(i+1)     # 微博排名
            num = str(item.find('span')).replace(
                '<span>', '').replace('</span>', '')  # 微博热度
            title = item.find('a').text  # 微博内容
            result.append(rank)
            result.append(num)
            result.append(title)
            # print(result)
            with open('/home/tamako/Desktop/allin/weibopy/static/datas/hot.csv', 'a+', newline='') as f:
                f_csv = csv.writer(f)        
                f_csv.writerow(result)
    
    def get_data_from_json(self,t):
        s = urllib.parse.quote(t)
        urls = "https://m.s.weibo.com/ajax_topic/detail?click_from=searchpc&q=%23{}%23".format(s)
        # print(urls)
        html = requests.get(urls, headers=self.headers).text
        datas = json.loads(html)
        Summarys = datas["data"]["baseInfo"]["object"]["summary"]
        addrs = datas["data"]["baseInfo"]["object"]["target_url"]
        categorys = datas["data"]["baseInfo"]["object"]["category"]
        auther = datas["data"]["baseInfo"]
        # print(auther)
        keys = []
        for key in auther:
            keys.append(key)
        if "claim_info" in keys:
            auther = auther["claim_info"]
            if auther == []:
                auther = ""
            else:
                auther = datas["data"]["baseInfo"]["claim_info"]["verified_reason"]
        else:
            auther = []
        readers_1 = datas["data"]["baseData"]["r"]["val"]
        readers_2 = datas["data"]["baseData"]["r"]["unit"]
        speaker_1 = datas["data"]["baseData"]["m"]["val"]
        speaker_2 = datas["data"]["baseData"]["m"]["unit"]
        # ------------动态图
        s = urllib.parse.quote(t)
        urls = "https://m.s.weibo.com/ajax_topic/trend?q=%23{}%23&type=read&time=6m".format(
            s)
        html = requests.get(urls, headers=self.headers).text
        datas = json.loads(html)
        arry = datas["data"]["read"]

        return [auther, addrs, Summarys, categorys, readers_1, readers_2, speaker_1,speaker_2, arry]

    #利用name作为关键词搜索，找到目标信息的评论等详细信息
    def search_for_everyone(self,index):
        #取出所有的name
        df = pd.read_csv(self.json_path+'hot.csv', header=None)
        rows = df.values.tolist()
        names = []
        for i in rows:
            names.append(i[2])
        names = names[:10]
        print(names)
        #调用外部封装函数获得所有的块，评论
        search_all_with_name(index,names[index])
