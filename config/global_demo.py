import pymysql.cursors
import get_token


"""
声明全局变量
@lihuanhuan@focusmedia.cn
"""


global GL_TOKEN
GL_TOKEN = get_token.get_token()
"""
定义头文件为全局变量
"""
headers = {
    'Authorization': GL_TOKEN,
    'Content-Type': 'application/json',
    'Origin': 'https://ad-preonline.fmtest.tech',
    'Referer': 'https://ad-preonline.fmtest.tech/',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
global GL_HEADERS
GL_HEADERS = headers


"""
连接Pre数据库，定义数据库为全局变量
"""
connection = pymysql.connect(
    host='rm-uf636zdzhj6ka5q8f.mysql.rds.aliyuncs.com',
    port=3306,
    user='liuwei',
    passwd='Mhxzkhl@123',
    db='kuma_ad_group',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
global GL_CONNECTION
GL_CONNECTION = connection


"""
计划、单元相关变量定义
"""
'''定义ad_group的Base URL'''
global GL_URL_AD_GROUP
GL_URL_AD_GROUP = 'http://ad-group-internal-preonline.fmtest.tech'

'''定义城市ID,测试使用西安市'''
global GL_CITY_ID
GL_CITY_ID = '610100000000'

global GL_BUILDING_IDS
GL_BUILDING_IDS = []

global GL_REPORT_ID1_191738
GL_REPORT_ID1_191738 = '191738'

global GL_REPORT_ID2_186073
GL_REPORT_ID2_186073 = '186073'

global GL_DSPID1
GL_DSPID1 = '186073'

'''创建的计划最终要删除，定义一个全局的变量'''
global GL_DEL_CAMPAIGN_LIST
GL_DEL_CAMPAIGN_LIST = []


"""
定义ad_cycle的Base URL
"""
global GL_URL_AD_CYCLE
GL_URL_AD_CYCLE = 'http://ad-cycle-internal-preonline.fmtest.tech'

"""给当前发布期和下个发布期的ID赋值，运行前必须检查修改ad_cycle_id"""
global GL_CUR_AD_CYCLE_ID
global GL_NEXT_AD_CYCLE_ID
GL_CUR_AD_CYCLE_ID = '2019W44'
GL_NEXT_AD_CYCLE_ID = '2019W45'



