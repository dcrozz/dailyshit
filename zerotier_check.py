import requests
import json
from datetime import datetime
from time import time
bearer = ''
networkid = ''
header = {
    "Authorization":"bearer %s" %bearer
}
url = 'https://my.zerotier.com/api/v1/network/%s/member' %networkid

def time_delta(lastOnline):
    a = datetime.fromtimestamp(time())
    b = datetime.fromtimestamp(lastOnline/1000)
    return a-b

def color(text, color):
    if color == 'red':
        return '\33[91m' + text + '\33[0m'
    elif color == 'green':
        return '\33[92m' + text + '\33[0m'
    else:
        return text

s = requests.session()
members = s.get(url, headers = header ).content
members = json.loads(members)
for member in members:
    print('Name: ' + member['name'])
    print('IP: ' + member['config']['ipAssignments'][0])
    print('Last Seen: ', end="")
    print(color('Online','green') if member['online'] else color(str(time_delta(member['lastOnline'])),'red'))
    print('')
