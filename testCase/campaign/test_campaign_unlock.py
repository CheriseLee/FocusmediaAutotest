import global_demo
import unittest
import time
import os
import ad_campaign
"""
解锁计划，仅给计划解锁，不涉及其他字段处理
@lihuanhuan@focusmedia.cn
"""


class UnlockCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_unlock_campaign_success(self):
        """解锁一个审核状态的计划，解锁成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''审核计划'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')

        '''解锁计划'''
        result = ad_campaign.AdCampaign().unlock_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='解锁计划成功，状态码为200则用例通过')

    def test_unlock_campaign_fail(self):
        """解锁一个不存在的计划ID，解锁失败，提示计划不存在"""
        result = ad_campaign.AdCampaign().unlock_campaign('111')
        self.assertEqual(result.status_code, 400, msg='解锁计划失败，投放计划不存在')
        text = result.json()
        response_code = text["code"]
        self.assertEqual(response_code, "AdCampaignIsNull", msg='投放计划不存在')


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


