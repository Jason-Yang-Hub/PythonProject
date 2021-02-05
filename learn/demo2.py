# -*- codeing = utf-8 -*-
# @Time    :2021/01/09 0009 19:58
# @Author  :杨旺盛
# @File    :demo2.py
# @Software: PyCharm

#作业：石头剪子布

import random

t = ["剪刀","石头","布"]

while True:
    try:
        a = int(input("请输入：剪刀（0）、石头（1）、布（2） "))
        if a < 0 or a > 2:
            continue

        aStr = t[a]
        print("你的输入为：%s（%d）" %(aStr,a))

        b = random.randint(0, 2)
        bStr = t[b]
        print("随机生成为：%s（%d）" %(bStr,b))

        if a == b :
            print("哈哈，平局。")
        elif a == 0 and b == 2:
            print("哈哈，你赢了。")
        elif a == 2 and b == 0:
            print("哈哈，你输了。")
        elif a < b :
            print("哈哈，你输了。")
        else :
            print("哈哈，你赢了。")

        c = input("\n要再来一把么？(y/n)   ")
        if c != "y" :
            break
    except:
        print("请输入数字")





