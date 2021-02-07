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

    totalpage = 10
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
                temp = "".join(temp.split("\xa0"))
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
            bd = "".join(bd.split("\xa0"))
            data.append(bd.strip())

            datalist.append(data)

    #print(datalist)
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



#保存数据（Excel）
def saveDataExcel(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)

    infoTitle = ["排名","中文名称","别名","链接","图片链接","评分","评价人数","概况","相关信息"]
    for i in range(len(infoTitle)):
        sheet.write(0,i,infoTitle[i])

    for i in range(len(datalist)):
        rank = i + 1
        data = datalist[i]

        sheet.write(i+1,0,str(rank))
        for j in range(len(data)):
            sheet.write(i+1,j+1,data[j])

    book.save(savepath)

#保存数据（sqlite）
def saveDataDb(datalist,dbPath):
    init_db(dbPath)
    connect = sqlite3.connect(dbPath)
    cur = connect.cursor()

    sqlbegin = "insert into movie250 (name,oname,link,pic,rating,judge,inq,bd)\n"
    for i in range(len(datalist)):
        data = datalist[i]
        for j in range(len(data)):
            if j == 4 or j == 5:
                continue
            data[j] = '"' + data[j] + '"'

        temp = "values(" + ",".join(data) + ");"
        sql = sqlbegin + temp
        cur.execute(sql)

    connect.commit()
    connect.close()


#创建表
def init_db(dbPath):
    sql = '''
        create table if not exists movie250
        (
            id integer primary key autoincrement,
            name varchar ,
            oname varchar ,
            link text,
            pic text,
            rating numeric ,
            judge number ,
            inq text,
            bd text
        );
    '''

    connect = sqlite3.connect(dbPath)
    cursor = connect.cursor()
    cursor.execute("drop table movie250")
    cursor.execute(sql)
    connect.commit()
    cursor.close()
    connect.close()


def main():
    print("程序启动")

    baseurl = "https://movie.douban.com/top250?start="

    #1.爬取网页数据并解析
    datalist = getData(baseurl)

    #2.保存数据（Excel）
    # path = ".\\爬虫数据存储.xls"
    # saveDataExcel(datalist,path)

    #3.保存数据（sqlite）
    dbPath = "doubantop250.db"
    saveDataDb(datalist,dbPath)

if __name__ == '__main__':
    main()
    print("爬取完毕")