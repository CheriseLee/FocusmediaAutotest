import global_demo
import unittest
import time
import os
import ad_campaign
import ad_unit
"""
锁定计划，仅给计划加锁，不涉及其他字段处理
@lihuanhuan@focusmedia.cn
"""


class LockCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_lock_campaign_success(self):
        """计划下无任何单元，锁定成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''锁定计划'''
        result = ad_campaign.AdCampaign().lock_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='锁定计划成功，状态码为200则用例通过')

    def test_lock_campaign_fail(self):
        """计划下有意向中单元，审核失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下插入一个PENDING的候补单元'''
        unit_status = 'PENDING'
        ad_unit_id = ad_unit.AdUnit.insert_CANDIDATE_unit_toDB(ad_campaign_id, unit_status)

        '''审核计划'''
        result = ad_campaign.AdCampaign().lock_campaign(ad_campaign_id)
        content = result.json()
        self.assertEqual(result.status_code, 200, msg='锁定计划失败，状态码为200则用例通过')
        self.assertEqual(content['success'], False, msg='锁定计划失败，锁定成功状态值为false 则用例通过')
        ad_unit.AdUnit.delete_CANDIDATE_unit_fromDB(ad_unit_id)


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


