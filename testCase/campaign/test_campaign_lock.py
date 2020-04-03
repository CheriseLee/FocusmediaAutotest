import global_demo
import unittest
import time
import os
import ad_campaign
import ad_unit
import time_function
import pytest
"""
锁定计划，仅给计划加锁，不涉及其他字段处理
@lihuanhuan@focusmedia.cn
"""


class TestLockCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_lock_campaign_success(self):
        """计划下无任何单元，锁定成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''锁定计划'''
        result = ad_campaign.AdCampaign().lock_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='锁定计划成功，状态码为200则用例通过')

    def test_lock_campaign_fail(self):
        """计划下有意向中单元，锁定失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下插入一个PENDING的候补单元'''
        unit_status = 'PENDING'
        ad_unit_id = ad_unit.AdUnit.insert_CANDIDATE_unit_toDB(ad_campaign_id, unit_status)

        '''锁定计划'''
        result = ad_campaign.AdCampaign().lock_campaign(ad_campaign_id)
        content = result.json()
        self.assertEqual(result.status_code, 200, msg='锁定计划失败，状态码为200则用例通过')
        self.assertEqual(content['success'], False, msg='锁定计划失败，锁定成功状态值为false 则用例通过')
        ad_unit.AdUnit.delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_lock_wait_campaign_success(self):
        """锁定计划，计划下有待发布单元，锁定成功，单元状态无变化"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        ''' 创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下创建一个候补单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        duration_in_second = 5
        frequency = 300
        start_date = tomorrow
        end_date = tomorrow
        ad_unit_type = 'CANDIDATE'
        dsp = False
        suit_codes = global_demo.GL_SUIT_CODES[0]
        ad_campaign_id = ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        result = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type,
                                              dsp, suit_codes, ad_campaign_id, dsp_id, target_type)
        ad_unit_id = result.json()['adUnitId']
        '''确认单元'''
        ad_unit.AdUnit.confirm_unit(ad_unit_id)
        '''获取单元的auditStatus'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        audit_status = result['auditStatus']

        '''锁定计划'''
        result = ad_campaign.AdCampaign().lock_campaign(ad_campaign_id)
        content = result.json()
        self.assertEqual(result.status_code, 200, msg='锁定计划成功，状态码为200则用例通过')
        self.assertEqual(content['success'], True, msg='锁定计划成功，锁定成功状态值为True 则用例通过')
        '''再次获取单元的auditStatus'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_audit_status = result['auditStatus']
        '''检查单元审核状态不变'''
        self.assertEqual(audit_status, new_audit_status, msg='单元审核状态不变，用例通过')

        '''解锁计划，撤销锁位，删除单元，环境恢复'''
        result = ad_campaign.AdCampaign().unlock_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='解锁计划成功，状态码为200则用例通过')
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        ad_unit.AdUnit().delete_unit(ad_unit_id)



if __name__ == '__main__':

    pytest.main()

