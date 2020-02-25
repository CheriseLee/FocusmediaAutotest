import global_demo
import unittest
import time
import os
import ad_campaign
"""
创建计划，KA、空位、公益、物业
KA、空位仅支持智能屏报备号的创建
公益仅支持FPE中有效的合同号、报备号
物业无限制
@lihuanhuan@focusmedia.cn
"""


class CreateCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    """正常场景用例"""
    def test_create_ka_vacant_campaign_success(self):
        """使用智能屏报备号创建KA、空位计划，创建成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type_list = ["KA", "VACANT"]
        for campaign_type in campaign_type_list:
            refer_id=global_demo.GL_REFER_ID1
            campaign_name = int(round(time.time() * 1000000))
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            ad_campaign_id = result.text
            self.assertEqual(result.status_code, 200, msg='创建计划，状态码为200则用例通过')
            '''检查接口返回信息和创建信息相同'''
            result = ad_campaign.AdCampaign.search_campaign_info(ad_campaign_id)
            self.assertEqual(result['adCampaignId'], ad_campaign_id, msg='检查计划ID，相同则用例通过')
            self.assertEqual(result['adCampaignName'], str(campaign_name), msg='检查计划名称，相同则用例通过')
            self.assertEqual(result['adCampaignType'], campaign_type, msg='检查计划类型，相同则用例通过')
            self.assertEqual(result['auditStatus'], 'INITIAL', msg='检查计划初始状态，相同则用例通过')
            global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
            time.sleep(1)

    def test_create_nonprofit_campaign_success(self):
        """创建公益计划，创建成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        refer_id = 'E-1900042'
        campaign_type = 'NONPROFIT'
        campaign_name = int(round(time.time() * 1000000))
        note = 'I am note'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note)
        ad_campaign_id = result.text
        self.assertEqual(result.status_code, 200, msg='创建计划，状态码为200则用例通过')
        '''检查接口返回信息和创建信息相同'''
        result = ad_campaign.AdCampaign.search_campaign_info(ad_campaign_id)
        self.assertEqual(result['adCampaignId'], ad_campaign_id, msg='检查计划ID，相同则用例通过')
        self.assertEqual(result['adCampaignName'], str(campaign_name), msg='检查计划名称，相同则用例通过')
        self.assertEqual(result['adCampaignType'], campaign_type, msg='检查计划类型，相同则用例通过')
        self.assertEqual(result['auditStatus'], 'INITIAL', msg='检查计划初始状态，相同则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

    def test_create_building_campaign_success(self):
        """创建物业计划,计划名称长度为50，创建成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        refer_id = 'P404'
        campaign_type = 'PROPERTY'
        campaign_name = 'qwertyuiopasdfghjklzxcvbnm123456789012345678901234'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        self.assertEqual(result.status_code, 200, msg='创建计划，状态码为200则用例通过')
        '''检查接口返回信息和创建信息相同'''
        result = ad_campaign.AdCampaign.search_campaign_info(ad_campaign_id)
        self.assertEqual(result['adCampaignId'], ad_campaign_id, msg='检查计划ID，相同则用例通过')
        self.assertEqual(result['adCampaignName'], str(campaign_name), msg='检查计划名称，相同则用例通过')
        self.assertEqual(result['adCampaignType'], campaign_type, msg='检查计划类型，相同则用例通过')
        self.assertEqual(result['auditStatus'], 'AUDITED', msg='检查计划初始状态，相同则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

    def test_create_duplicate_name_campaign_success(self):
        """不同报备号下创建重名计划，创建成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        report_id_list = ["136381", "144705"]
        for refer_id in report_id_list:
            campaign_type = 'KA'
            campaign_name = "duplicate_name"
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            ad_campaign_id = result.text
            self.assertEqual(result.status_code, 200, msg='创建计划，状态码为200则用例通过')
            '''检查接口返回信息和创建信息相同'''
            result = ad_campaign.AdCampaign.search_campaign_info(ad_campaign_id)
            self.assertEqual(result['adCampaignId'], ad_campaign_id, msg='检查计划ID，相同则用例通过')
            self.assertEqual(result['adCampaignName'], str(campaign_name), msg='检查计划名称，相同则用例通过')
            self.assertEqual(result['adCampaignType'], campaign_type, msg='检查计划类型，相同则用例通过')
            self.assertEqual(result['auditStatus'], 'INITIAL', msg='检查计划初始状态，相同则用例通过')
            global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
            time.sleep(1)

    """异常场景用例"""
    def test_create_duplicate_name_campaign_fail(self):
        """同报备号下创建重名计划，创建失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        for i in (range(2)):
            refer_id=global_demo.GL_REFER_ID1
            campaign_name = 'test'
            campaign_type = 'KA'
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            if i == 0:
                self.assertEqual(result.status_code, 200, msg='创建计划，状态码为200则用例通过')
                global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
                time.sleep(1)
            elif i == 1:
                self.assertEqual(result.status_code, 400, msg='创建重名计划，状态码为400则用例通过')
                text = result.json()
                response_code = text["code"]
                self.assertEqual(response_code, "AdCampaignNameDuplicated", msg='创建重名计划，返回码为AdCampaignNameDuplicated则用例通过')

    def test_valid_reportid_campaign_fail(self):
        """使用无效的报备号创建KA、空位计划，创建失败----目前接口报InternalServerError，前端会过滤"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type_list = ["KA", "VACANT"]
        for campaign_type in campaign_type_list:
            refer_id = '99999999999'
            campaign_name = int(round(time.time() * 1000000))
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            self.assertEqual(result.status_code, 500, msg='无效报备号创建计划，状态码为500则用例通过')
            text = result.json()
            response_code = text["code"]
            self.assertNotEqual(response_code, "InternalServerError", msg='创建失败')
            global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
            time.sleep(1)

    def test_valid_reportid_campaign_fail1(self):
        """使用数据库中能找到但是状态是无效的报备号，创建KA、空位计划，创建失败----目前接口报InternalServerError，前端会过滤"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type_list = ["KA", "VACANT"]
        for campaign_type in campaign_type_list:
            refer_id = '170610'
            campaign_name = int(round(time.time() * 1000000))
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            self.assertEqual(result.status_code, 500, msg='无效报备号创建计划，状态码为500则用例通过')
            text = result.json()
            response_code = text["code"]
            self.assertNotEqual(response_code, "InternalServerError", msg='创建失败')
            global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
            time.sleep(1)

    def test_no_smart_reportid_campaign_fail(self):
        """使用非智能屏的报备号创建KA、空位计划，创建失败----目前接口报InternalServerError，前端会过滤"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type_list = ["KA", "VACANT"]
        for campaign_type in campaign_type_list:
            refer_id = '9614'
            campaign_name = int(round(time.time() * 1000000))
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            self.assertEqual(result.status_code, 500, msg='非智能屏报备号创建计划，状态码为500则用例通过')
            text = result.json()
            response_code = text["code"]
            self.assertNotEqual(response_code, "InternalServerError", msg='创建失败')
            global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
            time.sleep(1)

    """必选参数是否必选，等价类测试"""
    def test_no_reportid_campaign_fail(self):
        """不传报备号创建计划，报错，创建失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type = 'KA'
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = ''
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        self.assertEqual(result.status_code, 400, msg='请求错误，状态码为400则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
        time.sleep(1)

    def test_no_name_campaign_fail(self):
        """不传计划名称，报错，创建失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type = 'KA'
        refer_id = ''
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        self.assertEqual(result.status_code, 400, msg='请求错误，状态码为400则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
        time.sleep(1)

    def test_no_type_campaign_fail(self):
        """不传计划类型，报错，创建失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type = ''
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        self.assertEqual(result.status_code, 400, msg='请求错误，状态码为400则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
        time.sleep(1)

    """可输入参数边界值测试"""
    def test_name_length_campaign_fail(self):
        """计划名称长度 > 50，报错，创建失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type = 'KA'
        refer_id=global_demo.GL_REFER_ID1
        campaign_name = 'qwertyuiopasdfghjklzxcvbnm1234567890123456789012341'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        self.assertEqual(result.status_code, 400, msg='请求错误，状态码为400则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
        time.sleep(1)

    def test_name_length_campaign_fail(self):
        """备注长度 > 251，报错，创建失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        campaign_type = 'KA'
        refer_id=global_demo.GL_REFER_ID1
        note = 'qwertyuiopasdfghjklzxcvbnm123456789012345678901234qwertyuiopasdfghjklzxcvbnm123456789012345678901234' \
               'qwertyuiopasdfghjklzxcvbnm123456789012345678901234qwertyuiopasdfghjklzxcvbnm123456789012345678901234' \
               'qwertyuiopasdfghjklzxcvbnm1234567890123456789012341'
        campaign_name = 'name'
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note)
        self.assertEqual(result.status_code, 400, msg='请求错误，状态码为400则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(result.text)
        time.sleep(1)



if __name__ == '__main__':

    # 定义测试用例集
    test_dir = os.path.abspath('.')
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(discover)


