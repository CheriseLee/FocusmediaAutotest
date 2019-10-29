import requests
from requests.auth import HTTPBasicAuth
"""
获取token
@lihuanhuan@focusmedia.cn
"""


def get_token():

    token_header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    auth = HTTPBasicAuth('app', 'app-password')

    datas = {
        'grant_type': 'password',
        'username': 'lihuanhuan@focusmedia.cn',
        'password':  'lihh0727'
    }
    baseURL = 'http://auth-server-internal-preonline.fmtest.tech'
    loginURL = baseURL+'/oauth/token'
    result = requests.post(loginURL, data=datas, auth=auth, headers=token_header, verify=False)
    unit = result.json()
    token = unit['access_token']
    return token