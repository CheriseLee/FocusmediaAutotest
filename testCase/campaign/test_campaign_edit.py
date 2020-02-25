import global_demo
import unittest
import time
import os
import ad_campaign
"""
修改计划
同报备号下计划名称不允许重复
@lihuanhuan@focusmedia.cn
"""


class EditCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_edit_campaign_success(self):
        """不修改计划的任何信息，允许修改"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = int(round(time.time() * 1000000))
        campaign_type = 'KA'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''修改计划'''
        result = ad_campaign.AdCampaign.edit_campaign(ad_campaign_id, campaign_name, note='')
        self.assertEqual(result.status_code, 200, msg='修改计划，状态码为200则用例通过')

    def test_edit_campaign_success1(self):
        """修改计划的名称、备注和之前不同，允许修改"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = int(round(time.time() * 1000000))
        campaign_type = 'KA'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''修改计划'''
        result = ad_campaign.AdCampaign.edit_campaign(ad_campaign_id, campaign_name='change', note='change')
        self.assertEqual(result.status_code, 200, msg='修改计划，状态码为200则用例通过')

    def test_edit_campaign_fail(self):
        """修改计划的名称和报备号下其他计划重复，修改失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建第一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = 'lihhtest'
        campaign_type = 'KA'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)

        '''创建第二个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_name1 = 'lihhtest1'
        campaign_type = 'KA'
        result1 = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name1, campaign_type, note='')
        ad_campaign_id1 = result1.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id1)

        '''修改计划2的名称和计划1相同,修改失败'''
        result = ad_campaign.AdCampaign.edit_campaign(ad_campaign_id1, campaign_name, note='')
        self.assertEqual(result.status_code, 400, msg='修改计划，状态码为400则用例通过')
        text = result.json()
        response_code = text["code"]
        self.assertEqual(response_code, "AdCampaignNameDuplicated", msg='计划名称重复，返回码为AdCampaignNameDuplicated则用例通过')

    def test_edit_unexist_campaign_fail(self):
        """修改的计划ID不存在，修改失败"""
        result = ad_campaign.AdCampaign.edit_campaign(ad_campaign_id='212', campaign_name='323', note='')
        self.assertEqual(result.status_code, 400, msg='修改计划，状态码为400则用例通过')
        text = result.json()
        response_code = text["code"]
        self.assertEqual(response_code, "AdCampaignIsNull", msg='计划ID不存在，返回码为AdCampaignIsNull则用例通过')

    def test_edit_campaign_name_null_fail(self):
        """修改计划的名称为空，修改失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建第一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = 'lihhtest'
        campaign_type = 'KA'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)

        '''修改计划的名称为空,修改失败'''
        result = ad_campaign.AdCampaign.edit_campaign(ad_campaign_id, campaign_name='', note='')
        self.assertEqual(result.status_code, 400, msg='修改计划，状态码为400则用例通过')
        text = result.json()
        response_code = text["code"]
        self.assertEqual(response_code, "BadRequest", msg='计划名称为空，返回码为BadRequest则用例通过')


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


