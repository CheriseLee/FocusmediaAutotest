import requests
import global_demo
import pymysql.cursors

def del_campaign_without_unit():
    """删除数据库里单元数为0的计划"""
    cursor = global_demo.GL_CONNECTION.cursor()
    '''查找数据库里所有的计划ID'''
    sql = "SELECT ad_campaign_id from ad_campaign"
    '''执行sql语句，避免sql执行失败产生死锁'''
    try:
        cursor.execute(sql)
        ad_campaign_list = cursor.fetchall()
        global_demo.connection.commit()
    except Exception as e:
        global_demo.connection.rollback()
    need_del_list = []
    n = 10000
    print(ad_campaign_list)
    for key in ad_campaign_list:
        payload = {
            "adCampaignIdList": [key['ad_campaign_id']],
            "pageNo": 1,
            "pageSize": n
        }
        list_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/list'
        result = requests.post(list_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        info = result.json()['result'][0]
        unit_count = info['adUnitCount']
        if unit_count == 0:
            need_del_list.append(key['ad_campaign_id'])
    for campaign in need_del_list:
        sql = "DELETE FROM ad_campaign WHERE ad_campaign_id='%s'"%campaign
        print(sql)
        '''执行sql语句，避免sql执行失败产生死锁'''
        try:
            cursor.execute(sql)
            global_demo.connection.commit()
        except Exception as e:
            global_demo.connection.rollback()

del_campaign_without_unit()

