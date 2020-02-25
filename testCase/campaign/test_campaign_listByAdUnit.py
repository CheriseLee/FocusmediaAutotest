import global_demo
import unittest
import time
import os
import ad_campaign
import ad_unit
import datetime
import time_function
"""
查询锁位未审核，急播过期计划
@lihuanhuan@focusmedia.cn
"""


class ListUnlockCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_list_unlock_campaign_success(self):
        """查看锁位未审核计划，查询结果非空，查询成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''计划下创建一个候补意向中单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        result = ad_unit.AdUnit().create_ka_guaranteed_building_unit(goal_location_num=10)
        ad_unit_id = result.json()['adUnitId']
        ad_campaign_id= result.json()['adCampaignId']
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)
        '''查询锁位未审核计划'''
        list_by_ad_unit_campaign = ad_campaign.AdCampaign().unaudit_campaign_list(start_date=tomorrow, end_date=tomorrow, initial_reserved="true", urgent_expired="false")
        '''检查创建的计划在查询列表中'''
        self.assertIn(ad_campaign_id, list_by_ad_unit_campaign, msg='对比相等，则用例通过')
        '''撤销锁位'''
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_list__urgent_campaign_success(self):
        """查看急播过期计划，查询结果非空，查询成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''计划下创建一个必播单元'''
        result = ad_unit.AdUnit().create_ka_guaranteed_building_unit(goal_location_num=10)
        ad_unit_id = result.json()['adUnitId']
        ad_campaign_id = result.json()['adCampaignId']
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)

        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()
        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)
        '''审核为急播单'''
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id=ad_campaign_id, contract_no= 'contract_no', contract_type= 'URGENT', brand='',
                                                         industry='', pb_content='', audit_type='')
        '''查询急播过期计划'''

        list_by_ad_unit_campaign = ad_campaign.AdCampaign().unaudit_campaign_list(start_date, end_date, initial_reserved="false", urgent_expired="true")
        '''检查创建的计划在查询列表中'''
        self.assertIn(ad_campaign_id, list_by_ad_unit_campaign, msg='对比相等，则用例通过')

        '''解锁计划，撤销锁位，删除单元，环境恢复'''
        result = ad_campaign.AdCampaign().unlock_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='解锁计划成功，状态码为200则用例通过')
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_list_unlock_urgent_campaign_fail(self):
        """锁位未审核false，急播过期false，查询结果为空"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''计划下创建一个必播单元'''
        result = ad_unit.AdUnit().create_ka_guaranteed_building_unit(goal_location_num=10)
        ad_unit_id = result.json()['adUnitId']
        ad_campaign_id = result.json()['adCampaignId']
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)

        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()
        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)
        '''审核为急播单'''
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id=ad_campaign_id, contract_no='contract_no', contract_type='URGENT', brand='',
                                                         industry='', pb_content='', audit_type='')
        '''查询急播过期计划'''
        ad_campaign.AdCampaign().unaudit_campaign_list(start_date, end_date, initial_reserved="false", urgent_expired="false")
        '''撤销锁位'''
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_list_unlock_urgent_campaign_success(self):
        """锁位未审核true，急播过期true，查询结果非空"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''计划下创建一个必播单元'''
        result = ad_unit.AdUnit().create_ka_guaranteed_building_unit(goal_location_num=10)
        ad_unit_id = result.json()['adUnitId']
        ad_campaign_id = result.json()['adCampaignId']
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)

        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)

        '''创建一个计划'''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id1 = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id1)
        time.sleep(1)
        '''急播计划下创建一个候补单元'''

        result = ad_unit.AdUnit().create_ka_candidate_suit_unit()
        ad_unit_id1 = result.json()['adUnitId']
        ad_campaign_id1 = result.json()['adCampaignId']
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id1)
        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id1)

        '''审核为急播单'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id1, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        '''查询锁位未审核和急播过期计划'''
        list_by_ad_unit_campaign = ad_campaign.AdCampaign().unaudit_campaign_list(start_date, end_date, initial_reserved="true", urgent_expired="true")
        '''检查创建的计划在查询列表中'''
        self.assertIn(ad_campaign_id, list_by_ad_unit_campaign, msg='对比相等，则用例通过')
        self.assertIn(ad_campaign_id1, list_by_ad_unit_campaign, msg='对比相等，则用例通过')
        
        '''解锁计划，撤销锁位，删除单元，环境恢复'''
        result = ad_campaign.AdCampaign().unlock_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='解锁计划成功，状态码为200则用例通过')
        result = ad_campaign.AdCampaign().unlock_campaign(ad_campaign_id1)
        self.assertEqual(result.status_code, 200, msg='解锁计划成功，状态码为200则用例通过')
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        ad_unit.AdUnit().revert_unit(ad_unit_id1)
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)
        ad_unit.AdUnit().delete_unit(ad_unit_id1)


if __name__ == '__main__':
    # 构造测试集
    # discover = unittest.TestSuite()
    # discover.addTest(createCampaign("test_createKaVacantCampaign_success"))
    # print(discover)

    # 按方法名构造用例集
    # 定义测试用例集

    test_dir = os.path.abspath('.')
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(discover)


