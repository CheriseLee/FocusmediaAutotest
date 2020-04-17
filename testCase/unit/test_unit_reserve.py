import ad_unit
import unittest
import ad_campaign
import global_demo
import time_function
import os

"""
锁位
@lihuanhuan@focusmedia.cn
"""


class TestReserveUnit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_reserve_not_pending_unit(self):
        '''单元状态为“待发布”、“已取消”、“已终止”、“发布中”、“发布完成”，给出提示，无法锁位'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建待发布单元'''
        create_info = ad_unit.AdUnit.create_ka_guaranteed_suit_unit()
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        # global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)

        '''必播项目挑点单元锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''已锁位单元再次锁位'''
        reserve_info_wait = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response_wait = reserve_info_wait.json()
        self.assertEqual(reserve_response_wait["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

        '''取消单元'''
        ad_unit.AdUnit.cancel_unit(ad_unit_id)
        '''已取消单元再次锁位'''
        reserve_info_cancel = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response_cancel = reserve_info_cancel.json()
        self.assertEqual(reserve_response_cancel["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

        '''创建发布中单元'''
        today = time_function.GetTime.get_today()
        create_info = ad_unit.AdUnit.create_ka_guaranteed_suit_unit(start_date=today,end_date=today)
        response = create_info.json()
        ad_unit_id1 = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]

        '''必播项目挑点单元锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id1)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''发布中单元再次锁位'''
        reserve_info_show = ad_unit.AdUnit().reserve_unit(ad_unit_id1)
        reserve_response_show = reserve_info_show.json()
        self.assertEqual(reserve_response_show["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

        '''终止单元'''
        ad_unit.AdUnit.terminate_unit(ad_unit_id1)
        '''已终止单元再次锁位'''
        reserve_info_cancel = ad_unit.AdUnit().reserve_unit(ad_unit_id1)
        reserve_response_cancel = reserve_info_cancel.json()
        self.assertEqual(reserve_response_cancel["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')


    '''候补可抢占'''
    def test_candidate_reserve_fail(self):
        '''候补可抢占单元、候补非抢占单元，锁位失败'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建候补可抢占单元'''
        create_info = ad_unit.AdUnit.create_ka_candidate_suit_unit()
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertEqual(reserve_response["code"], "AdUnitTypeCanNotReserve", msg='检查锁位失败，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

        '''创建候补非抢占单元'''
        create_info = ad_unit.AdUnit.create_vacant_non_candidate_suit_unit()
        response = create_info.json()
        ad_unit_id1 = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id1)
        reserve_response = reserve_info.json()
        self.assertEqual(reserve_response["code"], "AdUnitTypeCanNotReserve", msg='检查锁位失败，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id1)


if __name__ == '__main__':

    test_dir = os.path.abspath('.')
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(discover)