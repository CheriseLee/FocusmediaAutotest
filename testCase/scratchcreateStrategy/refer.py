import requests
import global_demo


token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzA1OTA5MzcsInVzZXJfaWQiOiIzNzVhNGE4YmYwMDY0ZWM2ODI2MDk2ODE5NzlmZGYzNiIsInVzZXJfbmFtZSI6IkUwMDEzNTM4IiwianRpIjoiNjk3ZjUwNzNiYjY4MTUwNDAwNDRiNzhhNTVkNGNkNGMiLCJjbGllbnRfaWQiOiJ3ZWIiLCJzY29wZSI6W119.mS1lRDUbXaGCZpsjyNdqbrzI0zWNglYzsP2nJ3DnwdMLU-OY-O-W6u775I9iKWsPHhjxiQHgKgHOsYZzVMhFTF_jF5e7rRA_FnzisIxu-aZAjy8Ib_O7ROUSNDt3X9hHeQmHEA4-h6-6mImHPzsD19YK6kHQ3LWxo098SlbMVzgFm9Xz7mLYM0FB2PmY9kTdCoFYgaHtGS0zRQwqo6jp_bc_rvNx4A4GgJvq7o4EvmE5qG-w5maMSca6jSAj5UESSt0XgCBkXzNum2nk9xdhnY7rrFHTXkf-h9uMou-eIqy0D6belYjq5woc6J89AogXTpaXJgrFFxI6z3dhTvpmncLg84KwudIdrWUZXbWKl0A-83jbZER2NbmFvSPLG_ljvS5KO-mBdUjltsRcHgl2Vkd2XqEZt3y8WZGBwqFpk9Jod8IOfZs6LSEq1fuSwWwl5wPOUX78qDV8U5AIfh4k-6ybKDmrmBvmbMB09Nnx4gpKGSctm4CHn8hR1IfVpQJgcvgXJKFdyijqODMHKKLIryiuOqS085-uZ98eBkO-fAi8jeSS88puB7ZR1920zmU7UO4A-qv9EmBKyYSccxWPLRQLAsNYV1GqP0s5KGH1z0Dg08FwI490hBUlpxVVT-y6vCP-0EddnbIbVuyaPXVO3ZNNgxrdb5uXQzzBc7Aeh50'


#定义头文件为全局变量
headers = {
    'Authorization': token,
    'Content-Type': 'application/json',
    'Origin': 'http://auth-server.internal.focusmedia.tech',
    'Referer': 'http://auth-server.internal.focusmedia.tech',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
payload = {
    "reportId": 136685
}
print(payload)
createCampaign = "http://auth-server.internal.focusmedia.tech/v1/ka-account/getReportInfoListByReportIdOrReportName"
result = requests.get(createCampaign, json=payload, headers=headers, verify=False)

print(result.json())