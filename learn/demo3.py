# -*- codeing = utf-8 -*-
# @Time    :2021/01/09 0009 21:15
# @Author  :杨旺盛
# @File    :demo3.py
# @Software: PyCharm

'''
#1-100求和
total = 0
min = 1
max = 100
num = min

while num <= max:
    total += num
    num += 1

print("%d到%d的总和=%d" %(min,max,total))

'''

#作业：用for循环和while循环输出九九乘法表
'''
for i in range(1,10):
    for j in range(1,10):
        if i > j:
            print("%d*%d=%d" % (i, j, i * j), end="\t")
        else:
            print("%d*%d=%d" % (i, j, i * j))
            break
'''

i = 1
max = 10
while i < max:
    j = 1
    while j < max:
        if i > j:
            print("%d*%d=%d" % (i, j, i * j), end="\t")
        else:
            print("%d*%d=%d" % (i, j, i * j))
            break
        j += 1
    i += 1