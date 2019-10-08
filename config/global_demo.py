# 获取token
import requests
import pymysql.cursors



#取token参数，定义token为全局变量
payload = {
    "client_id": 'E0013538',
    "client_secret": 'lihh0727',
    "grant_type": 'authorization_code',
    "code": "authorization_code",
}
# baseURL='http://auth-server-internal-preonline.fmtest.tech'
# loginURL = baseURL+'/oauth/token'
# result = requests.post(createUnitUrl, json=payload, headers=headers, verify=False)
# unit = result.json()


token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1Njk4MjY1MTMsInVzZXJfaWQiOiJmZDI3OWZkMTE1MGM0Mjg4YmQwZDAyZjFjYzZjMWI1YyIsInVzZXJfbmFtZSI6IkUwMDEzNTM4IiwianRpIjoiM2I4MjIw' \
        'ZDY3YTg4ODY0NDYxZGYwMmYwZGZkZmI2NGQiLCJjbGllbnRfaWQiOiJ3ZWIiLCJzY29wZSI6W119.ITeHm9fzATT_d9Z5Vt0LGaKXmRoY0m9wpkYoLjT8mYxwRd53ixGThrEd_7hmnBzchabg6tj7gEIkaGoQTlcGHDJzGYtYGr' \
        'CE3R9-czXKrLMbXNVJbThnI6ArQQMbc2QRSOX1ViDAdh_ZSg8ycQJiP_uL5ilgcaYG5Im2uxma0Ogz_yurBNfFTgcho20lPiDaPVatmfQu89IpzGpp8dToh8G1Zjq9UZIx9zIBV3F_49EiN2INO9FTkWNjDV14qqs4ktOWDz' \
        '4FFod2NZ6niQCiBIIYq5iD6cw3GbfEm4LYV8XYdAreIxUcnP9Vbsu0vvxoAmu9Sqa8XNxxM1IvNqIcQ'
global GL_token
GL_token= token

#定义头文件为全局变量
headers = {
    'Authorization': GL_token,
    'Content-Type': 'application/json',
    'Origin': 'https://ad-preonline.fmtest.tech',
    'Referer': 'https://ad-preonline.fmtest.tech/',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

global GL_headers
GL_headers=headers


#连接Pre数据库，定义数据库为全局变量
connection = pymysql.connect(
    host='rr-uf6i8rq4er9rt9acp.mysql.rds.aliyuncs.com',
    port=3306,
    user='kuma_rd_readonly',
    passwd='TGYzbLZUZW93rTRlTsPx',
    db='kuma_ad_group',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

global GL_connection
GL_connection = connection

global GL_baseURL_ad_Group
GL_baseURL_ad_Group = 'http://ad-group-internal-preonline.fmtest.tech'

global GL_delCampaignList
GL_delCampaignList = []