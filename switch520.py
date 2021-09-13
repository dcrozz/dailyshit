import requests
header = {
    # ':authority': 'switch520.com',
    # ':method': 'POST',
    # ':path': '/wp-admin/admin-ajax.php',
    # ':scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'content-length': '49',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': '',
    'origin': 'https://switch520.com',
    'referer': 'https://switch520.com/',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
content = {   
    'action': 'user_login',
    'username': 'xxx',
    'password': 'xxx'
}
url = 'https://switch520.com/wp-admin/admin-ajax.php'
s = requests.session()
login = s.post(url= url, headers=header, data = content)
header2 ={
    # ':authority': 'switch520.com',
    # ':method': 'POST',
    # ':path': '/wp-admin/admin-ajax.php',
    # ':scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'content-length': '19',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://switch520.com',
    'referer': 'https://switch520.com/%e7%ad%be%e5%88%b0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
content2 = {
    'action': 'user_qiandao'
}
res2 = s.post(url= url, headers=header2, data = content2, cookies = login.cookies)
print(res2.content.decode('unicode_escape'))