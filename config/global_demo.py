import pymysql.cursors
import get_token
import requests


def environment_pre_cn():
    global GL_TOKEN
    GL_TOKEN = get_token.get_pre_cn_token()

    """
    定义头文件为全局变量
    """
    headers = {
        'Authorization': GL_TOKEN,
        'Content-Type': 'application/json',
        'Origin': 'https://ad-preonline.fmtest.tech',
        'Referer': 'https://ad-preonline.fmtest.tech/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'ca-app-id': '12344'
    }
    global GL_HEADERS
    GL_HEADERS = headers

    global GL_API_ACCOUNTID
    GL_API_ACCOUNTID = '6924c8f8df2b4dadbd51b7d895f15274'

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
    定义各模块的Base URL
    """
    '''定义ad_group的Base URL'''
    global GL_URL_AD_GROUP
    GL_URL_AD_GROUP = 'http://ad-group.preonline.internal.fmtest.tech'

    '''定义ad_cycle的Base URL'''
    global GL_URL_AD_CYCLE
    GL_URL_AD_CYCLE = 'http://ad-cycle.preonline.internal.fmtest.tech'

    '''定义ad_strategy的Base URL'''
    global GL_URL_AD_STRATEGY
    GL_URL_AD_STRATEGY = 'http://ad-strategy.preonline.internal.fmtest.tech'

    '''定义creative的Base URL'''
    global GL_URL_AD_CREATIVE
    GL_URL_AD_CREATIVE = 'http://creative.preonline.internal.fmtest.tech'

    '''定义resource的Base URL'''
    global GL_URL_AD_RESOURCE
    GL_URL_AD_RESOURCE = 'http://ad-resource.preonline.internal.fmtest.tech'

    '''定义product的Base URL'''
    global GL_URL_PRODUCT
    GL_URL_PRODUCT = 'http://product.preonline.internal.fmtest.tech'

    '''定义opemAPI的Base URL'''
    global GL_URL_OPEN_API
    GL_URL_OPEN_API = 'http://openapi.preonline.internal.fmtest.tech'

    '''定义inventory的Base URL'''
    global GL_URL_OPEN_INVENTORY
    GL_URL_OPEN_INVENTORY = 'http://inventory.preonline.internal.fmtest.tech'

    global GL_URL_ORDER
    GL_URL_ORDER = 'http://order.preonline.internal.fmtest.tech'

    '''定义城市ID,测试使用中山市'''
    global GL_CITY_ID
    GL_CITY_ID = '442000000000'

    '''中山市A\B套套装编码'''
    global GL_SUIT_CODES
    GL_SUIT_CODES = ['EA300101', 'EA300148', 'EA300116', 'EA300163']

    global GL_BUILDING_IDS
    GL_BUILDING_IDS = ['5009136', '5009135', '5009134']

    global GL_REFER_ID1
    GL_REFER_ID1 = '186073'

    global GL_REFER_ID2
    GL_REFER_ID2 = '191738'

    global GL_DSPID1
    GL_DSPID1 = '29f2678825c447aebc2667e5aeed879d'

    global GL_DSPID2
    GL_DSPID2 = '86fb9ce3e28d4d599e68b3fab4b69be6'

    global GL_NONPROFIT_ID
    GL_NONPROFIT_ID= 'E-1800265'

    global GL_PROPERTY_ADMINID
    GL_PROPERTY_ADMINID = 'P3029339'
    #点位均可售
    global GL_PROPERTY_LOCATION_IDS
    GL_PROPERTY_LOCATION_IDS = ["8516112","8516113","8516114","8516115","8516116","8516118","8516130","8516090","8516126",
                                "8516096","8516097","8516099","8516101","8516105","8516125","8516128","8516087","8516093",
                                "8516092","8516107","8516108","8516109","8516120","8516086","8516088","8516102","8516123",
                                "8516094","8516110","8516111","8516117","8516103","8516095","8516119","8516104","8516122",
                                "8516129","8516089","8516091","8516098","8516100","8516106","8516121","8516124"]

    '''创建的计划最终要删除，定义一个全局的变量'''
    global GL_DEL_CAMPAIGN_LIST
    GL_DEL_CAMPAIGN_LIST = []

    '''第二个城市（珠海）的资源信息,点位均可售'''
    global GL_CITY_ID1
    GL_CITY_ID1 = '610100000000'

    global GL_PROPERTY_LOCATION_IDS1
    GL_PROPERTY_LOCATION_IDS1 = ["7867647", "7868227", "7868235", "7868237"]


def environment_sandbox_cn():
    global GL_TOKEN
    GL_TOKEN = get_token.get_sandbox_cn_token()
    """
    定义头文件为全局变量
    """
    headers = {
        'Authorization': GL_TOKEN,
        'Content-Type': 'application/json',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'ca-app-id':'12344'
    }
    global GL_HEADERS
    GL_HEADERS = headers

    global GL_API_ACCOUNTID
    GL_API_ACCOUNTID = 'cc60166efaed49a599c1fc5462edbcc1'

    global GL_PRODUCT_NAME
    GL_PRODUCT_NAME = 'EASYHOME'

    """
    连接sandbox-cn数据库，定义数据库为全局变量
    """
    connection = pymysql.connect(
        host='rm-uf6t3483v2xbdo38y.mysql.rds.aliyuncs.com',
        port=3306,
        user='root',
        passwd='Mhxzkhl@321',
        db='kuma_ad_group',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    global GL_CONNECTION
    GL_CONNECTION = connection

    """
    各模块的相关变量定义
    """
    '''定义ad_group的Base URL'''
    global GL_URL_AD_GROUP
    GL_URL_AD_GROUP = 'http://ad-group.internal.fmtest.tech'

    '''定义ad_strategy的Base URL'''
    global GL_URL_AD_STRATEGY
    GL_URL_AD_STRATEGY = 'http://ad-strategy.internal.fmtest.tech'

    '''定义ad_cycle的Base URL'''
    global GL_URL_AD_CYCLE
    GL_URL_AD_CYCLE = 'http://ad-cycle.internal.fmtest.tech'

    '''定义resource的Base URL'''
    global GL_URL_AD_RESOURCE
    GL_URL_AD_RESOURCE = 'http://ad-resource.internal.fmtest.tech'

    '''定义creative的Base URL'''
    global GL_URL_AD_CREATIVE
    GL_URL_AD_CREATIVE = 'http://creative.internal.fmtest.tech'

    '''定义product的Base URL'''
    global GL_URL_PRODUCT
    GL_URL_PRODUCT = 'http://product.internal.fmtest.tech'

    '''定义openAPI的Base URL'''
    global GL_URL_OPEN_API
    GL_URL_OPEN_API = 'http://openapi.internal.fmtest.tech'

    '''定义inventory的Base URL'''
    global GL_URL_INVENTORY
    GL_URL_INVENTORY = 'http://inventory.internal.fmtest.tech'
    '''定义order的Base URL'''
    global GL_URL_ORDER
    GL_URL_ORDER = 'http://order.internal.fmtest.tech'

    '''定义城市ID,测试使用中山市'''
    global GL_CITY_ID
    GL_CITY_ID = '442000000000'

    '''中山市A\B套套装编码'''
    global GL_SUIT_CODES
    GL_SUIT_CODES = ['EA300101','EA300148','EA300116','EA300163']

    global GL_BUILDING_IDS
    GL_BUILDING_IDS = ['5009136','5009135','5009134']

    global GL_REFER_ID1
    GL_REFER_ID1= '136730'

    global GL_REFER_ID2
    GL_REFER_ID2 = '136317'

    global GL_NONPROFIT_ID
    GL_NONPROFIT_ID= 'E-1800265'

    global GL_PROPERTY_ADMINID
    GL_PROPERTY_ADMINID = 'P3029339'

    global GL_PROPERTY_LOCATION_IDS
    GL_PROPERTY_LOCATION_IDS = ["8516112","8516113","8516114","8516115","8516116","8516118","8516130","8516090","8516126",
                                "8516096","8516097","8516099","8516101","8516105","8516125","8516128","8516087","8516093",
                                "8516092","8516107","8516108","8516109","8516120","8516086","8516088","8516102","8516123",
                                "8516094","8516110","8516111","8516117","8516103","8516095","8516119","8516104","8516122",
                                "8516129","8516089","8516091","8516098","8516100","8516106","8516121","8516124"]
    global GL_DSPID1
    GL_DSPID1 = '29f2678825c447aebc2667e5aeed879d'

    global GL_DSPID2
    GL_DSPID2 = '86fb9ce3e28d4d599e68b3fab4b69be6'

    '''创建的计划最终要删除，定义一个全局的变量'''
    global GL_DEL_CAMPAIGN_LIST
    GL_DEL_CAMPAIGN_LIST = []

    '''第二个城市（珠海）的资源信息,点位均可售'''
    global GL_CITY_ID1
    GL_CITY_ID1 = '610100000000'

    global GL_PROPERTY_LOCATION_IDS1
    GL_PROPERTY_LOCATION_IDS1 = ["7867647", "7868227", "7868235", "7868237"]


def environment_online_cn():
    global GL_TOKEN
    GL_TOKEN = get_token.get_online_cn_token()

    """
    定义头文件为全局变量
    """
    headers = {
        'Authorization': GL_TOKEN,
        'Content-Type': 'application/json',
        'Origin': 'https://ad-preonline.fmtest.tech',
        'Referer': 'https://ad-preonline.fmtest.tech/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'ca-app-id': '12344'
    }
    global GL_HEADERS
    GL_HEADERS = headers

    global GL_API_ACCOUNTID
    GL_API_ACCOUNTID = '6924c8f8df2b4dadbd51b7d895f15274'

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
    定义各模块的Base URL
    """
    '''定义ad_group的Base URL'''
    global GL_URL_AD_GROUP
    GL_URL_AD_GROUP = 'http://ad-group.internal.focusmedia.tech'

    '''定义resource的Base URL'''
    global GL_URL_AD_RESOURCE
    GL_URL_AD_RESOURCE = 'http://ad-resource.preonline.internal.fmtest.tech'









environment_sandbox_cn()
# environment_pre_cn()


"""
# def get_initial_environment():
    '''获取当前及下个发布周期ID',删除对应城市的全部订单数据'''

    global GL_CUR_AD_CYCLE_ID
    global GL_NEXT_AD_CYCLE_ID
    get_adCycleId = GL_URL_AD_CYCLE + '/v1/adCycle?limit=2&productName=SMART_SCREEN'
    result = requests.get(get_adCycleId, headers=GL_HEADERS, verify=False)
    print(result.json())
    GL_CUR_AD_CYCLE_ID = result.json()[1]["id"]
    GL_NEXT_AD_CYCLE_ID = result.json()[0]["id"]

    '''解除当前发布期和下个发布期的发布锁'''
    delete_adCycleLock = GL_URL_AD_CYCLE + '/v1/adCycle/lock/' + str(GL_CITY_ID) + GL_CUR_AD_CYCLE_ID
    result = requests.delete(delete_adCycleLock, headers=GL_HEADERS, verify=False)

    '''获取当前城市下所有的待发布、发布中单元，取消或终止掉'''
    cursor = GL_CONNECTION.cursor()
    '''查找待发布、发布中单元所在的计划，取消审核'''
    sql="SELECT ad_campaign_id FROM ad_unit WHERE city_id='%s' and ad_unit_status in('WAIT','SHOW') GROUP BY ad_campaign_id"%GL_CITY_ID
    '''执行sql语句，避免sql执行失败产生死锁'''
    try:
        cursor.execute(sql)
        campaignidList=cursor.fetchall()
        GL_CONNECTION.commit()
    except Exception as e:
        GL_CONNECTION.rollback()


    '''解锁所有涉及的计划'''
    for key in campaignidList:
        unlock_campaign = GL_URL_AD_GROUP + '/v1/ad/campaign/unLock/' + key['ad_campaign_id']
        requests.post(unlock_campaign, headers=GL_HEADERS, verify=False)

    '''查找待发布单元并取消'''
    sql = "SELECT ad_unit_id FROM ad_unit WHERE city_id='%s' and ad_unit_status in('WAIT')" % GL_CITY_ID
    try:
        cursor.execute(sql)
        adunitidList = cursor.fetchall()
        GL_CONNECTION.commit()
    except Exception as e:
        GL_CONNECTION.rollback()

    for key in adunitidList:
        cancel_unit = GL_URL_AD_GROUP + '/v1/ad/unit/cancel/' + key['ad_unit_id']
        requests.post(cancel_unit, headers=GL_HEADERS, verify=False)

    '''查找发布中单元并终止'''
    sql = "SELECT ad_unit_id FROM ad_unit WHERE city_id='%s' and ad_unit_status in('SHOW')" % GL_CITY_ID
    try:
        cursor.execute(sql)
        adunitidList = cursor.fetchall()
        GL_CONNECTION.commit()
    except Exception as e:
        GL_CONNECTION.rollback()

    for key in adunitidList:
        payload ={
            "adUnitId": key
        }
        terminate_unit = GL_URL_AD_GROUP + '/v1/ad/unit/terminate'
        requests.post(terminate_unit, json=payload, headers=GL_HEADERS, verify=False)


"""


