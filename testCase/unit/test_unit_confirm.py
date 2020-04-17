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


class TestConfirmUnit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_confirm_not_pending_unit(self):
        '''单元状态为“待发布”、“已取消”、“已终止”、“发布中”、“发布完成”，给出提示，无法确认'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建待发布单元'''
        create_info = ad_unit.AdUnit.create_ka_candidate_suit_unit()
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        confirm_info = ad_unit.AdUnit().confirm_unit(ad_unit_id)
        self.assertEqual(confirm_info.status_code,200,  msg='检查确认成功，则用例通过')

        '''待发布单元再次确认'''
        confirm_info_wait = ad_unit.AdUnit().confirm_unit(ad_unit_id)
        confirm_response_wait = confirm_info_wait.json()
        self.assertEqual(confirm_response_wait["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

        '''取消单元'''
        ad_unit.AdUnit.cancel_unit(ad_unit_id)
        '''已取消单元再次确认'''
        confirm_info_cancel = ad_unit.AdUnit().confirm_unit(ad_unit_id)
        confirm_response_cancel = confirm_info_cancel.json()
        self.assertEqual(confirm_response_cancel["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

        '''创建发布中单元'''
        today = time_function.GetTime.get_today()
        create_info = ad_unit.AdUnit.create_ka_candidate_suit_unit(start_date=today,end_date=today)
        response = create_info.json()
        ad_unit_id1 = response["adUnitId"]

        '''必播项目挑点单元锁位'''
        confirm_info = ad_unit.AdUnit().confirm_unit(ad_unit_id1)
        self.assertEqual(confirm_info.status_code, 200,  msg='检查确认成功，则用例通过')
        '''发布中单元再次锁位'''
        confirm_info_show = ad_unit.AdUnit().confirm_unit(ad_unit_id1)
        confirm_response_show = confirm_info_show.json()
        self.assertEqual(confirm_response_show["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

        '''终止单元'''
        ad_unit.AdUnit.terminate_unit(ad_unit_id1)
        '''已终止单元再次锁位'''
        confirm_info_cancel = ad_unit.AdUnit().confirm_unit(ad_unit_id1)
        confirm_response_cancel = confirm_info_cancel.json()
        self.assertEqual(confirm_response_cancel["code"], "AdUnitStatusCanNotReserve", msg='检查锁位失败，则用例通过')

    def test_guaranteed_confirm_fail(self):
        '''必播单元单元，不支持确认，确认失败'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建必播意向中单元'''
        create_info = ad_unit.AdUnit.create_ka_guaranteed_suit_unit()
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''确认'''
        confirm_info = ad_unit.AdUnit().confirm_unit(ad_unit_id)
        confirm_response = confirm_info.json()
        self.assertEqual(confirm_response["code"], "AdUnitTypeCanNotConfirm", msg='检查锁位失败，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)


if __name__ == '__main__':

    test_dir = os.path.abspath('.')
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(discover)