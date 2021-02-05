# -*- coding = utf-8 -*-
# @Time    :2021/01/30 0030 00:13
# @Author  :杨旺盛
# @File    :spider.py
# @Software: PyCharm

from bs4 import BeautifulSoup           #网页解析，获取数据
import re                               #正则表达式，进行文字匹配
import urllib.request,urllib.error      #制定URL，获取网页数据
import xlwt                             #进行Excel操作
import sqlite3                          #进行SQLite数据库操作

#影片标题
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片链接
findLink = re.compile(r'<a href="(.*?)">')
#影片图片的路径
findImage = re.compile(r'<img.*src="(.*?)"',re.S)
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评分人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#影片概况
findInq = re.compile(r'<span class="inq">(.*?)</span>')
#影片其他内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)



#爬取网页数据并解析
def getData(baseurl):
    datalist = []

    totalpage = 1
    pernum = 25
    for i in range(0,totalpage):
        # 爬取网页
        url = baseurl + str(i * pernum)
        html = askURL(url)

        # 解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"):
            data = []
            item = str(item)
            # print(item)

            title = re.findall(findTitle,item)
            data.append(title[0])
            if len(title) > 1:
                temp = title[1].replace("/"," ")
                data.append(temp)
            else:
                data.append("")

            link = re.findall(findLink,item)[0]
            data.append(link)

            imgSrc = re.findall(findImage, item)[0]
            data.append(imgSrc)

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            judge = re.findall(findJudge, item)[0]
            data.append(judge)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                data.append(inq[0].replace("。"," "))
            else:
                data.append("")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd)
            bd = re.sub('/',' ',bd)
            data.append(bd.strip())

            datalist.append(data)

    print(datalist)
    return datalist

#得到指定网页URL内容
def askURL(url):
    #用户代理（模拟浏览器信息）
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 84.0.4147.89Safari / 537.36"
    }

    req = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
        # print(html)
        return html
    except urllib.error.URLError as err:
        if hasattr(err,"code"):
            print(err.code)
        if hasattr(err,"reason"):
            print(err.reason)



#存储数据
def saveData(savepath):
    pass



def main():
    print("程序启动")

    baseurl = "https://movie.douban.com/top250?start="
    savepath = ".\\豆瓣电影Top250.xls"

    #1.爬取网页数据并解析
    datalist = getData(baseurl)

    #2.保存数据
    saveData(savepath)

if __name__ == '__main__':
    main()