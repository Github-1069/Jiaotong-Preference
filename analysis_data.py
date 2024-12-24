import os
import pandas as pd

data_path=os.path.join(os.getcwd(),'raw_data1.csv')
fgr=pd.read_csv(data_path)
n=len(fgr)
trash=['序号','提交答卷时间', '所用时间', '来源', '来源详情', '来自IP', '总分']
property=['1、你的性别：', '2、你的专业：', '3、你的年级：', '4、你的生源地','5、你每月的零花钱大概是']

# 1 for short, 2 for medium, 3 for long
distance={
    0:['7','9','11','12'],
    1:['6','13','16','17'],
    2:['8','10','14','15']
}

# 0 for sunny, 1 for rainy
weather={
    0:['6','7','9','10','14','17'],
    1:['8','11','12','13','15','16']
}

# 0 for leisure, 1 for hurry
timelmt={
    0:['6','9','10','12','13','17'],
    1:['7','8','11','14','15','16']
}

for i in trash:
    del(fgr[i])
fgr[fgr=='(空)']=0

namelist=fgr.columns
for i in namelist:
    if len(i)>13:
        fgr.rename(columns={i:i[0:4]+'地铁/公交车'},inplace=True)
print(fgr.columns)