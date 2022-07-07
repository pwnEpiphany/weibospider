import json
import urllib
import requests
import threading
from Spider import *
from login import loginClient

# k = loginClient()
# cookie = k.main("18975957357","lsp49929")

cookie = {'Cookies': 'ALC=ac=2&bt=1655952302&cv=5.0&et=1687488302&ic=-543943304&login_time=1655952302&scf=&uid=7460837832&vf=0&vs=1&vt=0&es=b20027e2143226551d274daff8193ad9; LT=1655952302; tgc=TGT-NzQ2MDgzNzgzMg==-1655952302-gz-6B5C7CFAFE0A3C0AC32FE701ADBF0F1D-1; SRF=1655952303; SRT=D.QqHBJZPAWDSAQrMb4cYGS4SIisSHdZYuU!PuMDSHNEYdV3Y1NOipMERt4EP1RcsrA4uJP!XtTsVuObEu4ciIMZMCKDicVqizNOVrd!HaO!bnOGMiSEYOWrsI*B.vAflW-P9Rc0lR-ykgDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPWfSZiJNDH3S-uGRqE-AOYcSeWbNQfti4uzMD!s44uOTGm3JdYbOZEfS4PQVqMmVdigic!kIdi9IQ9ETNrpVF!kI4u9IdbqT4klSc!kIPH9N-uZT4kli-!kI4u9NroQT4kldF!kIdS9N3!pT4klJF!kIOM9N-uKT4kuTF!kIOM9IQ9NT4kJVn77; ALF=1687488302; SUB=_2A25Pt6P_DeRhGeFK7VIZ8ynEyD6IHXVsxJI3rDV8PUJbmtANLVH8kW9NQyRcKF4B83fs3HI74ZB_NIpLtMdXSwMK; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whf3LH2wgnGc1vA8ffweIz85NHD95QNShq71heN1heEWs4Dqcj6i--ci-zEi-2pi--Ni-isiKnfi--RiKnciKn7i--NiKLWiKnXi--fiKy2iKn0i--4iKnNiKyhi--4i-zRiKLs; SSOLoginState=1655952303'}
# p = spider(cookie["Cookies"])
# p.Hotsearch()
# p.search_for_everyone(0)
dic = {"one":0,"two":1,"three":2,"four":3,"five":4,"six":5,"seven":6,"eight":7,"nine":8,"ten":9}
idx = 0
# with open("/home/tamako/Desktop/allin/weibopy/local/cookie.json",'r') as f:
#     cookie = json.loads(f.read())

hot = spider(cookie["Cookies"])
hot.Hotsearch()
hot.search_for_everyone(idx)
with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(idx),'r') as f:
    datas = json.loads(f.read())
print(datas)
# p.search_for_everyone()
# class myThread (threading.Thread):
#     def __init__(self, threadID, index,name, idx,ids,mids):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.ids = ids
#         self.mids = mids
#         self.idx = idx
#         self.index = index
#     def run(self):
#         print ("开始线程：" + self.name)
#         search_details(self.idx,self.ids,self.mids)
#         print ("退出线程：" + self.name)


# headers = {"Cookie": "_T_WM=63609169492; XSRF-TOKEN=dc15ea; WEIBOCN_FROM=1110006030; MLOGIN=0; M_WEIBOCN_PARAMS=oid%3D4774734652506260%26luicode%3D10000011%26lfid%3D102803",
#  "host": "m.weibo.cn", "proxys": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"}
    
# def get_json_from_url(url):
#     html = requests.get(url, headers=headers).text
#     datas = json.loads(html)
#     return datas

# def search_for_everyone(name):
#     url1 = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%253D1%2526q%253D{}&page_type=searchall".format(urllib.parse.quote(name))
#     datas = get_json_from_url(url1) 
#     ids = []
#     mids = []
#     for i in range(1,11):
#         roots = datas["data"]["cards"][i]
#         keys = []
#         for key in roots:
#             keys.append(key)
#         # print(keys)
#         if "mblog" in keys:
#             ids.append(datas["data"]["cards"][i]["mblog"]["id"])
#             mids.append(datas["data"]["cards"][i]["mblog"]["mid"])
#         elif "card_group" in keys:
#             rooots1 = datas["data"]["cards"][i]["card_group"]
#             str1 = str(rooots1)
#             try:
#                 kk = str1.index("'mid': ")
#                 kk1 = str1.index("'id': ")
#                 mids.append(str(str1[kk+8:kk+24]))
#                 ids.append(str(str1[kk1+7:kk1+23]))
#             except:
#                 continue
#         else:
#             print("wrong")
#             break
#     return ids,mids

#     #json文件格式
#     #name{
#     #    id:
#     #    mid:
#     #    detail:
#     #    comment:[0，1，2，3，4，5，6，7，8，9]   
#     #}
# def search_details(idx,ids,mids):
#     detail_url = "https://m.weibo.cn/statuses/extend?id={}".format(ids)
#     comment_url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(ids,mids)
#     answer_json = {"id":ids,"mid":mids}
#     details = get_json_from_url(detail_url)
#     comment = get_json_from_url(comment_url)
#     detail = details["data"]["longTextContent"]
#     comments = []
#     if comment["ok"] == 0:
#         comments = []   
#     else:
#         max_len = len(comment["data"]["data"])
#         if max_len >=10:
#             for i in range(10):
#                 kk = {"name":comment["data"]["data"][i]["user"]["screen_name"],"text":comment["data"]["data"][i]["text"]}
#                 comments.append(kk)
#         else:
#             for i in range(max_len):
#                 kk = {"name":comment["data"]["data"][i]["user"]["screen_name"],"text":comment["data"]["data"][i]["text"]}
#                 comments.append(kk)
#     answer_json["detail"] = detail
#     answer_json["comment"] = comments
#     datadict = json.dumps(answer_json)
#     with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(idx+10),'w') as f:
#         f.write(datadict)

# def search_all_with_name(index,name):
#     ids = []
#     mids = []
#     threads = []
#     ids,mids = search_for_everyone(name)
#     for i in range(len(ids)):
#         threads.append(myThread(index,i,"Thread-{}".format(i),i,ids[i],mids[i]))
#     for th in threads:
#         th.start()
#     for en in threads:
#         en.join()
#     print("search over")
#     total_dict = {"name":name}
#     content = []
#     for i in range(len(ids))
#         with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(index),'w') as f1: 
#             for i in range(len(ids))
#                 with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(i+10),'r') as f:       
#                     file = json.loads(f)
#                     content.append(file)
#             total_dict{"content":content}
#             tmp = json.dumps(total_dict)
#                 f1.write(tmp)

# def search_for_everyone():
#     #取出所有的name
#     df = pd.read_csv("/home/tamako/Desktop/allin/weibopy/static/datas/hot.csv", encoding='gbk', header=None)
#     rows = df.values.tolist()
#     names = []
#     for i in rows:
#         names.append(i[2])
#     print(names)
#     #调用外部封装函数获得所有的块，评论
#     for j in range(len(nam
#         es)):
#         search_all_with_name(j,names[j])


