import re 
import pandas as pd
import requests
import threading
import os
import jieba
import wordcloud
import time
from urllib import parse
from urllib import request
from collections import Counter
from pprint import pprint

# 设置存储文件名
word = '古网帖子'

# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
import imageio
mk = imageio.imread("gujian.png")

# 构建并配置词云对象w，注意要加stopwords集合参数，将不想展示在词云中的词放在stopwords集合里
w = wordcloud.WordCloud(width=800,
                        height=600,
                        background_color='white',
                        font_path='msyh.ttc',
                        mask=mk,
                        scale=7,
                        max_words=140,
                        relative_scaling=0,
                        stopwords={'标题','楼主','发布','时间','链接','https','baidu','tieba','固定','个'})

header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Connection':'keep-alive'
}
cookies ='taihe=49f804bf599e1d2e7097ddaab9346b02; gdt_fp=b12882fe899d997513066e6299159850; Hm_lvt_7f3c7021befced5794c58fb4cdf1e85c=1583155914; UM_distinctid=171c06df82363f-0cb9cb485a2cd5-7373667-240000-171c06df82462e; ngacn0comUserInfo=%25CA%25A2%25CF%25C4%25C2%25CC%25D2%25F1%09%25E7%259B%259B%25E5%25A4%258F%25E7%25BB%25BF%25E8%258D%25AB%0939%0939%09%0910%090%094%090%090%09; taihe_bi_sdk_uid=138ff2b7a025e641db6fe24343d8c5d6; ngaPassportUid=60098929; ngaPassportUrlencodedUname=%25CA%25A2%25CF%25C4%25C2%25CC%25D2%25F1; ngaPassportCid=X8s0gvdp3k8r4t6orle5rncamtcdgl09tmb6ghbi; _178i=1; ngacn0comUserInfoCheck=6e20d88ffd5c9067af895e15b4543afc; ngacn0comInfoCheckTime=1598751847; taihe_bi_sdk_session=70587c578eea9c593c1e610e1827a6c4; CNZZDATA30043604=cnzz_eid%3D1219455781-1554826246-null%26ntime%3D1598753170; lastvisit=1598753326; lastpath=/thread.php?fid=618&page=; bbsmisccookies=%7B%22pv_count_for_insad%22%3A%7B0%3A-35%2C1%3A1598806810%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1598806810%7D%2C%22uisetting%22%3A%7B0%3A%22c%22%2C1%3A1598753623%7D%7D; _cnzz_CV30043604=forum%7Cfid618%7C0'
cookie = {}
for line in cookies.split(';'):
    name, value = cookies.strip().split('=', 1)
    cookie[name] = value

#   发起请求获得指定页数的主题
def getTopic(number):
    topics = []
    for i in range(1,number+1):
        url='https://nga.178.com/thread.php?fid=618&page='+str(i)
        print(url)
        html = requests.get(url=url, cookies=cookie,headers=header).content.decode('gb18030')
        movie_item = re.findall(r'class=\'topic\'>(.*?)<\/a>', html,re.S) 
        print(len(movie_item))
        topics=topics+movie_item
        print(topics)
        #   写入文件
        with open(word + '.txt','w',encoding='utf-8')as f:
            f.write(format(topics))
        time.sleep(1)
    return topics

getTopic(10)

# 对来自外部文件的文本进行中文分词，得到string
f = open('古网帖子.txt',encoding='utf-8')
txt = f.read()
txtlist = jieba.lcut(txt)
string = " ".join(txtlist)

# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)

# 将词云图片导出到当前文件夹
w.to_file('古剑词云.png')

# counter = Counter(txtlist)

# pprint(counter.most_common(10))
