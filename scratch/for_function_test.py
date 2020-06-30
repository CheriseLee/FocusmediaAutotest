import global_demo
import unittest
import time
import os
import ad_campaign
import time_function
import ad_unit
import requests
import sys
import os
import json
"""
解锁计划，仅给计划解锁，不涉及其他字段处理
@lihuanhuan@focusmedia.cn
"""


'''构建锁位未审核计划'''
def create_many_campaign():
    for i in range(10000):

        '''创建一个计划'''
        refer_id = '136730'
        campaign_type = 'KA'
        campaign_name = 'lihhtest'+time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_type,campaign_name,  note='')
        ad_campaign_id = result.text
        time.sleep(1)
        for i in range(10):

            '''创建一个候补单元'''
            ad_unit_type ='CANDIDATE'
            ad_unit_target_ids = global_demo.GL_BUILDING_IDS
            target_type = 'BUILDING'
            response = ad_unit.AdUnit().create_pure_unit(ad_campaign_id,ad_unit_type, ad_unit_target_ids, target_type)
            ad_unit_id = response.json().get('adUnitId')

            payload = {}
            '''确认'''
            confirm_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/confirm/' + ad_unit_id
            requests.post(confirm_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)

'''按单元ID查询创意，5000条单元，分别多个创意，测试效率'''
def getCreativeGroupIdsByAdUnitIds():

    '''创建一个计划'''
    refer_id = '136730'
    campaign_type = 'KA'
    campaign_name = 'lihhtest'+time.strftime("%Y-%m-%d %H_%M_%S")
    result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
    ad_campaign_id = result.text
    for i in range(10000):
        '''创建一个候补单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        ad_unit_id = create_unit(duration_in_second=15, frequency=2500, start_date=tomorrow,
                                                       end_date='2021-12-25', ad_unit_type='CANDIDATE',
                                                       dsp=False, suit_codes=['EA300178'], ad_campaign_id=ad_campaign_id,
                                                       dsp_id=global_demo.GL_DSPID1, target_type='SUIT')

        payload = {}
        '''确认'''
        confirm_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/confirm/' + ad_unit_id
        requests.post(confirm_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)



'''批量创建必播单'''
def GUARANTEED():

    '''创建一个计划'''
    refer_id = '136730'
    campaign_type = 'KA'
    campaign_name = 'lihhtest'+time.strftime("%Y-%m-%d %H_%M_%S")
    result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
    ad_campaign_id = result.text
    for i in range(2000):
        '''创建一个必播单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        ad_unit_id = create_unit(duration_in_second=15, frequency=300, start_date=tomorrow,
                                                       end_date='2021-12-25', ad_unit_type='GUARANTEED',
                                                       dsp=False, ad_unit_target_ids=['EA300178'], ad_campaign_id=ad_campaign_id,
                                                       dsp_id=global_demo.GL_DSPID1, target_type='CITY')

        payload = {
            "adUnitId": ad_unit_id
        }
        '''锁位'''
        confirm_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/reserve/'
        requests.post(confirm_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)


'''批量创建目标级排播，生成targetset文件'''
def create_strategy_targetset_data():
    with open('location.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
        # if data.startswith(u'\ufeff'):
        #     content = data.encode('utf8')[3:].decode('utf8')
        # content = data.encode('utf8')[3:].decode('utf8')
        print(data)
        # f.seek(0, os.SEEK_CUR)
        # a = json.loads(content)
        lst = []
        # a 是一个list
        print(type(data))
        for key in data:
            targetset ={
                "id": "EA300101",
                "type": "BUILDING"
            }
            targetset['id']=key.strip('\n')
            lst.append(targetset)
        # print(lst)
        f.close()
    with open('locationTarget.txt', 'w+') as write_f:
        # for key in enumerate(lst):
        #     print(key)
        #     write_f.write(key[1] + '\n')
        write_f.write(str(lst))
    write_f.close()

'''批量创建计划，每个计划审核为不同的品牌'''
def create_campaign():
    for i in range(2):
        '''创建一个计划'''
        refer_id = '136730'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        # campaign_name = time.time()
        print(campaign_name)
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下插入一个候补单元'''
        ad_unit.AdUnit.insert_CANDIDATE_unit_toDB(ad_campaign_id, "WAIT")
        '''审核计划,审核成功'''
        contract_no = 'wytest'+str(i)
        contract_type = 'CONTRACT'
        brand = 'brand'+str(i)
        industry = 'industry'+str(i)
        pb_content = 'pb_content'+str(i)
        audit_type = 'audit_type'+str(i)
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand=brand,
                                                         industry=industry, pb_content=pb_content, audit_type=audit_type)

'''批量创建候补单'''
def create_candidate_units():
    '''创建一个计划'''
    # refer_id = '136730'
    # campaign_type = 'KA'
    # campaign_name = 'lihhtest' + time.strftime("%Y-%m-%d %H_%M_%S")
    # result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
    # ad_campaign_id = result.text
    for i in range(2400):
        '''创建一个候补单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        ad_unit_id = create_unit(duration_in_second=15, frequency=300, start_date=tomorrow,
                                 end_date='2020-04-12', ad_unit_type='CANDIDATE',
                                 dsp=False, ad_unit_target_ids=['404'], ad_campaign_id="136730_147215",
                                 dsp_id=global_demo.GL_DSPID1, target_type='BUILDING')

        '''确认'''
        confirm_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/confirm/'+str(ad_unit_id)
        requests.post(confirm_unit_url,  headers=global_demo.GL_HEADERS, verify=False)


if __name__ == '__main__':
    # create_many_campaign()
    starttime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(starttime)
    # getCreativeGroupIdsByAdUnitIds()
    # GUARANTEED()
    # create_strategy_targetset_data()
    create_many_campaign()
    endtime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(endtime)



