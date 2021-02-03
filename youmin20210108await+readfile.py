#!/usr/local/bin/python3
#-*-coding:UTF-8-*-
'''首先在python文件下创建一个叫youmin的文件夹'''
'''20200908改为requests库'''
'''20200923改为异步'''
'''20200925改为asyncio.run'''
'''20201203添加reafile功能，定义checkfolder，addtask，getfoldname等函数'''
'''20201206:优化全局变量名称，否则会urllist又重复取值'''
'''20210108:修改26行正则，添加对不同class、style、algin的适配；网页支持2021;修改178行为range(1,50)，去掉第0页；添加timeout'''
import re
import requests
import os
import random
import sys
import asyncio
import aiohttp
from aiohttp import TCPConnector
import aiofiles
from time import time

os.chdir('/Users/sycao/Downloads/aria2/sd/')

src='<img class="picact".*?src="(.*?)"'
detail='<img class="picact".*?</a><br>(.*?)</p>'
#修改网页中间部分获取正则，添加class和style的适配
member='<p(?: class="GsImageLabel" align="center"| | class="GsImageLabel" style="text\-align: center;"| style="text\-align: center;"| align="center")>.*?</p>'
titlelist=[]
urllist=[]
targeturls=[]
foldnames=[]
img=re.compile(src)
mem=re.compile(member)
tasks=[]

async def getimg(url,s,t):
#下载图片
    global img
    titles = ''
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=TCPConnector(ssl=False),timeout=timeout) as session:
            async with await session.get(url) as reponse:
                html = await reponse.text()
        ##这里还是一定要有个去\n的地方
        memlist=re.findall(mem,html.replace("\n",""))
        # print(memlist)
        # print(url)
        # print(html)
        for i in memlist:
            # print i
            imglist=re.findall(img,i)
            titles=re.findall(detail,i.replace('&nbsp; ','').replace('&nbsp;',''))
            # print(imglist)
            # if imglist == ['https://img1.gamersky.com/image2020/11/20201105_ls_red_141_3/gamersky_027small_054_20201151826435.jpg']:
            #     print(memlist)
            #     print(url)
            ####
            for j in imglist:
                #下载图片
                tit=titles[0] if len(titles)>0 else random.choice(["Make", "Love", "No", "War", "by", "John", "Lenon"])
                #去除字体,把斜杠换全角
                font=re.search(r'">(.*?)<',tit)
                tit=tit.replace('/','／') .replace('\\','＼') if font is None else font.group(1)
                # print(('./youmin/'+t+'/'+str(s)+"--"+tit+j[-4:]))
                async with aiofiles.open('./youmin/'+t+'/'+str(s)+"--"+tit+j[-4:],'wb') as f:
                    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                        async with await session.get(j) as reponse:
                            page_text = await reponse.read()
                    await f.write(page_text)
    except Exception as ex:
        print(url)
        print(imglist)
        print("title=", titles)
        print("\n出现如下异常%s"%ex, '\n')

def getbaseurl():
#获得当前5个地址
    url='https://www.gamersky.com/ent/'#游民每日图片发布页
    s = requests.get(url).content.decode('utf-8')
    urlhtm1='<a class="img1 countHit" target="_blank" .*?</a>'#寻找图片发布页网址所在的html区域
    urlhtm2='<a class="img2 countHit" target="_blank" .*?</a>'
    #  herfhtm='https:.*?shtml'#图片发布页网址
    herfhtm='http.*?shtml'#图片发布页网址
    datestr='gameshd/202[0|1]/(.*?)_.*?.jpg'
    title='<div class="txt">(.*?)</div>'
    urs1=re.compile(urlhtm1)
    urs2=re.compile(urlhtm2)
    # urs=re.compile(herfhtm)
    urllist1=re.findall(urs1,s)#查找所有最新图片发布页网址
    urllist2=re.findall(urs2,s)
    divlist=urllist1+urllist2

    for i in divlist:
        urllist.append(re.search(herfhtm,i).group())
        date = re.search(datestr,i).group(1)
        title1=re.search(title,i).group(1)
        titlelist.append(date + '-' + title1)

async def get_download_argv():
#根据输入判断获取模式    
    foldname =''
    if len(sys.argv) == 1:
        #没有参数输入，
        mode = eval(input('Please input number: \n0.Input URL manually \n1.Get the newest\n'))
        if mode != 0:
            getbaseurl()
            for i in range(5):
                print((str(i) + ' ' + titlelist[i]))
            num = eval(input('Please input number:'))
            targeturl= urllist[int(num)]
            foldname = titlelist[int(num)]
        else:
            targeturl = eval(input('Please input the URL:\n'))
            s = requests.get(targeturl).content.decode('utf-8')
            title = re.search('<h1>(.*?)</h1>',s).group(1)
            foldname = title
    elif sys.argv[1] == 'readfile':
        #读取
        targeturls = readfile()
        foldnames = []
        print(targeturls)
        for targeturl in targeturls:
            # s = requests.get(targeturl).content.decode('utf-8')
            # title = re.search('<h1>(.*?)</h1>',s).group(1)
            foldname = await getfoldname(targeturl)
            foldnames.append(foldname)
        return foldnames
    else:
        targeturl = sys.argv[1]
        foldname = getfoldname(targeturl)
    return targeturl, foldname

async def getfoldname(targeturl):
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with await session.get(targeturl) as reponse:
            s = await reponse.text()
    # s = requests.get(targeturl).content.decode('utf-8').replace('&nbsp; ','').replace('&nbsp;','').replace('\r\n','')
    title = re.search('<h1>(.*?)</h1>',s.replace('&nbsp; ','').replace('&nbsp;','').replace('\r\n','')).group(1)
    try:
        datestr = re.search('<div class="detail">\s*(.*?)\s',s).group(1)
    except:
        datestr = input('Input the date manually:')
    foldname = datestr + '-' + title
    return foldname

def readfile():
    urllist = []
    with open('urllist','r') as f:
        for i in f.readlines():
            urllist.append(i.strip())
    return urllist

    # s = requests.get(targeturl).content.decode('utf-8').replace('&nbsp; ','').replace('&nbsp;','').replace('\r\n','')
    # title = re.search('<h1>(.*?)</h1>',s).group(1)
    # try:
    #     datestr = re.search('<div class="detail">\s*(.*?)\s',s).group(1)
    # except:
    #     datestr = input('Input the date manually:')
    # foldname = datestr + '-' + title
    # return foldname, title

def checkfolder(foldname):
    if foldname in os.listdir('youmin'):
        for filename in os.listdir(os.path.join( 'youmin', foldname)):
            os.remove(os.path.join( 'youmin', foldname, filename ))
    elif foldname!='':    
        os.mkdir('./youmin/'+foldname)

def addtask(targeturl, foldname):
    #创建下载targeturl的前50页的任务，文件夹名为foldname
    for i in range(1,50):
        s=i
        if i==1:
            i=''
        else:
            i='_'+str(i)
        murl = targeturl[:-6]+str(i)+targeturl[-6:]
        c = getimg(murl, s, foldname)
        task = asyncio.create_task(c)
        tasks.append(task)

async def main():
    if len(sys.argv) != 1:
        if sys.argv[1] == 'readfile':
            targeturl = readfile()
            foldname = await get_download_argv()
            for url,fold in zip(targeturl, foldname):
                checkfolder(fold)
                addtask(url,fold)
        elif sys.argv[1] == 'today':
            getbaseurl()
            targeturl = urllist[0]
            foldname = titlelist[0]
            checkfolder(foldname)
            addtask(targeturl,foldname)
    else:
        targeturl, foldname = await get_download_argv()
        checkfolder(foldname)
        addtask(targeturl,foldname)
    await asyncio.gather(*tasks)

start = time()

asyncio.run(main())

end =time()
print ('Cost {} seconds'.format((end - start)))