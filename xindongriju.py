import requests

header = {
    'Host': 'www.doki8.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '54',
    'Origin': 'http://www.doki8.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'http://www.doki8.com/?s=%E6%BF%91%E6%88%B7%E5%86%85%E6%B5%B7',
    'Cookie': '',
    'Upgrade-Insecure-Requests': '1'
}

content = {
    "log": "xxx",
    "pwd": "xxx",
    "wp-submit": "登录"
}
url = 'http://www.doki8.com/wp-login.php'

s = requests.session()
res = s.post(url = url, headers = header, data = content)
print('登录成功' if res.content.decode('utf-8').find('登出') != -1 else '登录失败')