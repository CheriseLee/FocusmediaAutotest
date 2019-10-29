import global_demo
import unittest
import time
import os
import ad_campaign
import ad_unit
"""
删除计划
计划下无单元时支持删除（DELETE状态的除外）
@lihuanhuan@focusmedia.cn
"""


class DelCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_del_campaign_success(self):
        """计划下无任何单元，允许删除"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''删除计划'''
        result = ad_campaign.AdCampaign().del_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='删除计划，状态码为200则用例通过')

    def test_del_campaign_success1(self):
        """计划下只有delete状态的单元，允许删除"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下插入一个DELETE的候补单元'''
        unit_status = 'DELETED'
        ad_unit_id = ad_unit.AdUnit.insert_CANDIDATE_unit_toDB(ad_campaign_id, unit_status)
        '''删除计划'''
        result = ad_campaign.AdCampaign().del_campaign(ad_campaign_id)
        self.assertEqual(result.status_code, 200, msg='删除计划，状态码为200则用例通过')
        '''删除插入的候补单元'''
        ad_unit.AdUnit.delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_del_campaign_fail(self):
        """计划下有WAIT、PENDING、SHOW、CANCELLED、FINISH、TERMINATED状态的单元，不允许删除"""
        unit_status_list = ['WAIT', 'PENDING', 'SHOW', 'CANCELLED', 'FINISH', 'TERMINATED']
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        for unit_status in unit_status_list:
            '''创建一个计划'''
            refer_id = '136381'
            campaign_type = 'KA'
            campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            ad_campaign_id = result.text
            global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
            time.sleep(1)

            '''在计划下插入一个候补单元'''
            ad_unit_id = ad_unit.AdUnit.insert_CANDIDATE_unit_toDB(ad_campaign_id, unit_status)
            '''删除计划'''
            result = ad_campaign.AdCampaign().del_campaign(ad_campaign_id)
            self.assertEqual(result.status_code, 400, msg='删除计划失败，状态码为400则用例通过')
            '''删除插入的候补单元'''
            ad_unit.AdUnit.delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_del_noexist_campaign_fail(self):
        """删除不存在的计划ID，报错提示计划ID"""
        result = ad_campaign.AdCampaign().del_campaign('11111')
        self.assertEqual(result.status_code, 400, msg='删除计划失败，状态码为400则用例通过')


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


