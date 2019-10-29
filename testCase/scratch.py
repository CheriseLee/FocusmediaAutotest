import requests
import pymysql.cursors
import time


#配置预发数据库
connection = pymysql.connect(
    host='rm-uf636zdzhj6ka5q8f.mysql.rds.aliyuncs.com',
    port=3306,
    user='liuwei',
    passwd='Mhxzkhl@123',
    db='kuma_ad_group',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1Njk4MjY1MTMsInVzZXJfaWQiOiJmZDI3OWZkMTE1MGM0Mjg4YmQwZDAyZjFjYzZjMWI1YyIsInVzZXJfbmFtZSI6IkUwMDEzNTM4IiwianRpIjoiM2I4MjIw' \
        'ZDY3YTg4ODY0NDYxZGYwMmYwZGZkZmI2NGQiLCJjbGllbnRfaWQiOiJ3ZWIiLCJzY29wZSI6W119.ITeHm9fzATT_d9Z5Vt0LGaKXmRoY0m9wpkYoLjT8mYxwRd53ixGThrEd_7hmnBzchabg6tj7gEIkaGoQTlcGHDJzGYtYGr' \
        'CE3R9-czXKrLMbXNVJbThnI6ArQQMbc2QRSOX1ViDAdh_ZSg8ycQJiP_uL5ilgcaYG5Im2uxma0Ogz_yurBNfFTgcho20lPiDaPVatmfQu89IpzGpp8dToh8G1Zjq9UZIx9zIBV3F_49EiN2INO9FTkWNjDV14qqs4ktOWDz' \
        '4FFod2NZ6niQCiBIIYq5iD6cw3GbfEm4LYV8XYdAreIxUcnP9Vbsu0vvxoAmu9Sqa8XNxxM1IvNqIcQ'

#定义头文件为全局变量
headers = {
    'Authorization': token,
    'Content-Type': 'application/json',
    'Origin': 'https://ad-preonline.fmtest.tech',
    'Referer': 'https://ad-preonline.fmtest.tech/',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

#  查找数据库里所有已锁位、已审核必播单元的cityId、unitID
start_date = '2019-10-14'
end_date = '2019-10-14'
sql = "SELECT ad_unit_id,city_id from ad_unit WHERE  start_date <= '%s'  AND '%s' <= end_date AND ad_unit_status IN ('WAIT', 'SHOW') and ad_unit_type='GUARANTEED' and audit_status='AUDITED'"%(start_date,end_date)

# print(sql)
cursor = connection.cursor()
# 执行sql语句，避免sql执行失败产生死锁
try:
    cursor.execute(sql)
    searchResult = cursor.fetchall()
    unitInfo_list = []
    for key in searchResult:
        unitInfo_list.append(key)
    connection.commit()
except Exception as e:
    connection.rollback()
# print(unitInfo_list)
print(type(unitInfo_list))

# #根据单元ID、城市ID查找已锁点位数

for key in (unitInfo_list):
    payload ={
      "cityId":key['city_id'],
      "bizId":key['ad_unit_id']
    }
    # inquireLocation = 'http://inventory.internal.focusmedia.tech/v3/inventory/inquireLocation'
    inquireLocation = 'http://http://inventory-internal-preonline.fmtest.tech/v3/inventory/inquireLocation'
    result = requests.post(inquireLocation, json=payload, headers=headers, verify=False)
    print(result)
    time.sleep(3)