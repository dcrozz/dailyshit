'''
20200120 添加起始网页,下载课程数输入
20200202 添加选项模式（最新开始，从页面开始）,去除重复输出
20200203 添加序号，添加ffmpeg下载
TODO:
1. 睡眠时间(判断对应的js出了就好？）
2. 添加ffmpeg下载
'''

from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import sys
import os

print('Creating proxy server...')
server = Server('/Users/sycao/Downloads/dedao/browsermob-proxy-2.1.4/bin/browsermob-proxy')
server.port = 8090
server.start()
proxy = server.create_proxy()

options = webdriver.ChromeOptions()
options.add_argument('--headless')#无头模式，不开启游览器界面
options.add_argument("--mute-audio")#静音，出声音了笑死
options.add_argument('--proxy-server={0}'.format(proxy.proxy))
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
##################
# driver.implicitly_wait(10)
base_url = 'https://www.dedao.cn/article/g258WANERjwQJDzBjlKbOMG1rZqkPl'
proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})

if len(sys.argv) == 1:
    mode = input("Download Modes:\n0. From the Latest\n1. From specified URL\nPlease the Download Mode: ")
    course_url = 'https://www.dedao.cn/course/5L9DznlwYyOVdwasGdKmbWABv0Zk4a'
    i = input('Please the num of lessons: ')
    i = int(i)
elif sys.argv[1] == 'today':
    mode = "0"
    course_url = 'https://www.dedao.cn/course/5L9DznlwYyOVdwasGdKmbWABv0Zk4a'
    i = 1

#确保上一篇的按钮可以出来
driver.set_window_size(1920,1080)

if mode == "1":
    base_url = input('Please initial URL:\n')
    driver.get(base_url)
    #感觉js没载出来，第一个back按了没用
    time.sleep(10)
else:
    driver.get(course_url)
    time.sleep(5)
    try:
        print("Start find Content")
        ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//span[@class='content-tab']")))
        content_button = driver.find_element_by_xpath("//span[@class='content-tab']")
        content_button.click()
        time.sleep(5)
    except:
        print("Content button can't find")

    try:
        print("Start find Filter")
        ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@class='filter filter filter-select']/div[@class='bought-filter-right']")))
        filter_button = driver.find_element_by_xpath("//div[@class='filter filter filter-select']/div[@class='bought-filter-right']")
        filter_button.click()
        time.sleep(5)
    except:
        print("Filter button can't find")

    try:
        print("Start find Reverse")
        ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//li[@attr='inverted']")))
        reverse_button = driver.find_element_by_xpath("//li[@attr='inverted']")
        reverse_button.click()
        time.sleep(5)
    except:
        print("Reverse button can't find")

    try:
        print("Start find the first lesson")
        ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@class='content']//li[@class='single-content']")))
        first_lesson = driver.find_element_by_xpath("//div[@class='content']//li[@class='single-content']")
        first_lesson.click()
        #第一次进课程页死慢，back的js可能没加载出来
        time.sleep(10)
    except:
        print("The first lesson can't find")

#课程数量是
while i: 
    try:
        print(str(i) + ' ' + "Start Find Play")
        ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@class='dd-audio']//span[@class='iconfont iget-common-f4 iget-icon-play']")))
        play = driver.find_element_by_xpath("//div[@class='dd-audio']//span[@class='iconfont iget-common-f4 iget-icon-play']")
        play.click()
        print(str(i) + ' ' + "Play Clicked")
    except:
        print(str(i) + ' ' + "play button can't find")
    try:
        print(str(i) + ' ' + "Start Find Back")
        ele = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//aside[@class='iget-side-button iget-side-portrait']//div[@class='side-button-main']//button[@class='button iget-common-b4']")))
        back = driver.find_element_by_xpath("//aside[@class='iget-side-button iget-side-portrait']//div[@class='side-button-main']//button[@class='button iget-common-b4']")
        back.click()
        print(str(i) + ' ' + "Back Clicked")
        time.sleep(3)
    except:
        print(str(i) + ' ' + "back button can't find")
    i = i-1

print("OVER")
result = proxy.har
with open('3.har', 'w') as outfile:
    json.dump(proxy.har, outfile)


i=1
url_titles = []
for entry in result['log']['entries']:
    _url = entry['request']['url']
    # 根据URL找到数据接口
    try:
        if "mutiget_by_alias" in _url:
            _response = entry['response']
            j = json.loads(_response['content']['text'])
            _title   = j["c"]['list'][0]["title"]
            _content = j["c"]['list'][0]["mp3_play_url"]
            print(str(i) + '. ' + _title)
            print(_content)
            i = int(i) + 1
            url_titles.append([_title,_content])
    except:
        if "mutiget_by_alias" in _url:
            _response = entry['response']
            j = json.loads(_response['content']['text'])
            _title   = j["c"]['list'][0]["title"]
            print(_title)
        print(_url)
server.stop()
driver.quit()

i = int(input("Download From: "))
j = int(input("Download To: "))

for url_title in url_titles[i-1:j+1]:
    url = url_title[1]
    title = url_title[0]
    os.system('ffmpeg -protocol_whitelist "file,https,crypto,tcp,tls" -i {} -codec copy "{}.mp4"'.format(url,title))




