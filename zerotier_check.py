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

s = requests.session()
members = s.get(url, headers = header ).content
members = json.loads(members)
for member in members:
    print('Name: ' + member['name'])
    print('IP: ' + member['config']['ipAssignments'][0])
    print('Last Seen: ' + 'Online' if member['online'] else str(time_delta(member['lastOnline'])))
    print('')