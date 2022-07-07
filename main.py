#coding:utf-8
from app import app
from flask import request, render_template, jsonify, request, redirect, make_response
from flask.json import jsonify
from login import loginClient
import json
from Spider import spider
import Spider
import pandas as pd
import threading

class myThread (threading.Thread):
    def __init__(self,hot,name):
        threading.Thread.__init__(self)
        self.name = name
        self.hot = hot
    def run(self):
        print ("开始线程：" + self.name)
        self._return = get_dict(self.hot,self.name)
    def join(self):
        threading.Thread.join(self)
        return self._return

@app.route('/')
def hello_world():
    return render_template("index_normal.html")


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST'])
def lg():
    try:
        if request.method == "POST":
            username = request.form['username']
            passwd = request.form['password']
            # print(username)
            tmp = loginClient()
            cookie = tmp.main(username,passwd)["Cookies"]
            k = {"cookie":cookie}
            print(k)
            with open("/home/tamako/Desktop/allin/weibopy/local/cookie.json",'w') as f:
                kk = json.dumps(k)
                f.write(kk)
            print("####################################")
            return redirect("main")
        else:
            return render_template("index_normal.html")
    except:
        return render_template('404.html')


def format_data():
    df = pd.read_csv("/home/tamako/Desktop/allin/weibopy/static/datas/hot.csv", header=None)
    rows = df.values.tolist()
    result = []
    for j in rows[:10]:
        result.append({"name":j[2]})
    return result

def get_dict(hot,name):
    tmp = hot.get_data_from_json(name)
    abstract = tmp[2]
    auther = tmp[0]
    categorys = tmp[3]
    readers = str(tmp[4])+tmp[5]
    dic = {"name":name,"abstract":abstract, "auther":auther, "categorys":categorys, "readers":readers}
    return dic

@app.route('/main')
def index():
    cookie = ""
    with open("/home/tamako/Desktop/allin/weibopy/local/cookie.json",'r') as f:
        cookie = json.loads(f.read())

    if cookie == "":
        return render_template("index_normal.html")
    hot = spider(cookie["cookie"])
    hot.Hotsearch()
    result = format_data()
    threads = []
    final = []
    for j in range(len(result)):
        threads.append(myThread(hot,result[j]["name"]))
    for th in threads:
        th.start()
    for en in threads:
        final.append(en.join())

    # a = [{"name":"lsp11111111","abstract":"asdfasdfasdfasdf", "auther": "lsp", "categorys":"sdf", "readers":"10yi"}]
    #获得数据，传入页面，传入的是数组，数组内容是字典，每一个代表一个热搜，包含的数据是，名字，内容，热度，作者，reader
    return render_template("index.html", arry = final)

@app.route("/datas/<name>")
def show_data(name):
    dic = {"one":0,"two":1,"three":2,"four":3,"five":4,"six":5,"seven":6,"eight":7,"nine":8,"ten":9}
    idx = dic[name]
    with open("/home/tamako/Desktop/allin/weibopy/local/cookie.json",'r') as f:
        cookie = json.loads(f.read())

    hot = spider(cookie["cookie"])
    hot.search_for_everyone(idx)
    with open("/home/tamako/Desktop/allin/weibopy/static/datas/{}.json".format(idx),'r') as f:
        datas = json.loads(f.read())
    print(datas)
    keys = []
    for key in datas:
        keys.append(key)
    data = []
    if "content" in keys:
        data = datas["content"]
    else:
        data.append(datas)#列表
    """
    data [{}]
    data[idx]["detail"]#详细数据
    data[idx]["comment"]#评论 [{name,text}]
    """
    while (len(data) < 10):
        data.append({"id":"空了","mid":"空了","detail":"空了","comment":[]})
    for i in range(len(data)):
        while(len(data[i]["comment"]) < 10):
            data[i]["comment"].append({"name":"这里没有奥","text":"这里没有奥"})
    # print(data)
    return render_template("datas.html",datas=data)


if __name__ == '__main__':
    # server = make_server('127.0.0.1', 5000, app)
    # server.serve_forever()
    app.run(debug=True)
