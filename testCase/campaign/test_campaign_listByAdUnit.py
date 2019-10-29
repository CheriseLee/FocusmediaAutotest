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

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        new_ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(new_ad_campaign_id)
        time.sleep(1)

        '''计划下创建一个必播单元'''
        today = datetime.date.today()
        tomorrow = str(today + datetime.timedelta(days=1))
        duration_in_second = 5
        frequency = 300
        start_date = tomorrow
        end_date = tomorrow
        ad_unit_type = 'GUARANTEED'
        dsp = True
        suit_codes = ['EA300101']
        ad_campaign_id = new_ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        ad_unit_id = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, suit_codes, ad_campaign_id, dsp_id, target_type)

        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)
        '''查询锁位未审核计划'''
        initialreserved = "true"
        urgentexpired = "false"
        list_by_ad_unit_campaign = ad_campaign.AdCampaign().no_audit_campaign_list(start_date, end_date, initialreserved, urgentexpired)

        '''检查创建的计划在查询列表中'''
        self.assertIn(new_ad_campaign_id, list_by_ad_unit_campaign, msg='对比相等，则用例通过')

        '''撤销锁位'''
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_list__urgent_campaign_success(self):
        """查看急播过期计划，查询结果非空，查询成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        new_ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(new_ad_campaign_id)
        time.sleep(1)

        '''计划下创建一个必播单元'''
        today = datetime.date.today()
        tomorrow = str(today + datetime.timedelta(days=1))
        duration_in_second = 5
        frequency = 300
        start_date = tomorrow
        end_date = tomorrow
        ad_unit_type = 'GUARANTEED'
        dsp = True
        suit_codes = ['EA300101']
        ad_campaign_id = new_ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        ad_unit_id = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, suit_codes, ad_campaign_id, dsp_id, target_type)

        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)
        '''审核为急播单'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        '''查询急播过期计划'''
        initialreserved = "false"
        urgentexpired = "true"
        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()
        list_by_ad_unit_campaign = ad_campaign.AdCampaign().no_audit_campaign_list(start_date, end_date, initialreserved, urgentexpired)

        '''检查创建的计划在查询列表中'''
        self.assertIn(new_ad_campaign_id, list_by_ad_unit_campaign, msg='对比相等，则用例通过')

        '''撤销锁位'''
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_list_unlock_urgent_campaign_fail(self):
        """锁位未审核false，急播过期false，查询结果为空"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        new_ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(new_ad_campaign_id)
        time.sleep(1)

        '''计划下创建一个必播单元'''
        today = datetime.date.today()
        tomorrow = str(today + datetime.timedelta(days=1))
        duration_in_second = 5
        frequency = 300
        # start_date = tomorrow
        # end_date = tomorrow
        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()
        ad_unit_type = 'GUARANTEED'
        dsp = True
        suit_codes = ['EA300101']
        ad_campaign_id = new_ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        ad_unit_id = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, suit_codes, ad_campaign_id, dsp_id, target_type)

        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)
        '''审核为急播单'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        '''查询急播过期计划'''
        initialreserved = "false"
        urgentexpired = "false"
        # start_date = time_function.GetTime.get_next_next_monday()
        # end_date = time_function.GetTime.get_next_next_monday()
        list_by_ad_unit_campaign = ad_campaign.AdCampaign().no_audit_campaign_list(start_date, end_date, initialreserved, urgentexpired)
        print(list_by_ad_unit_campaign)

        '''撤销锁位'''
        ad_unit.AdUnit().revert_unit(ad_unit_id)
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_list_unlock_urgent_campaign_success(self):
        """锁位未审核true，急播过期true，查询结果非空"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        new_ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(new_ad_campaign_id)
        time.sleep(1)

        '''计划下创建一个必播单元'''
        today = datetime.date.today()
        tomorrow = str(today + datetime.timedelta(days=1))
        duration_in_second = 5
        frequency = 300
        # start_date = tomorrow
        # end_date = tomorrow
        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()
        ad_unit_type = 'GUARANTEED'
        dsp = True
        suit_codes = ['EA300101']
        ad_campaign_id = new_ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        ad_unit_id = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, suit_codes, ad_campaign_id, dsp_id, target_type)

        '''锁位'''
        ad_unit.AdUnit().reserve_unit(ad_unit_id)

        '''创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        new_ad_campaign_id1 = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(new_ad_campaign_id1)
        time.sleep(1)
        '''急播计划下创建一个候补单元'''
        today = datetime.date.today()
        tomorrow = str(today + datetime.timedelta(days=1))
        duration_in_second = 5
        frequency = 300
        # start_date = tomorrow
        # end_date = tomorrow
        start_date = time_function.GetTime.get_next_next_monday()
        end_date = time_function.GetTime.get_next_next_monday()
        ad_unit_type = 'CANDIDATE'
        dsp = True
        suit_codes = ['EA300101']
        ad_campaign_id = new_ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        ad_unit_id1 = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, suit_codes, ad_campaign_id, dsp_id, target_type)

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id1)

        '''审核为急播单'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        ad_campaign.AdCampaign().audit_campaign(new_ad_campaign_id1, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        '''查询锁位未审核和急播过期计划'''
        initialreserved = "true"
        urgentexpired = "true"
        # start_date = time_function.GetTime.get_next_next_monday()
        # end_date = time_function.GetTime.get_next_next_monday()
        list_by_ad_unit_campaign = ad_campaign.AdCampaign().no_audit_campaign_list(start_date, end_date, initialreserved, urgentexpired)
        '''检查创建的计划在查询列表中'''
        self.assertIn(new_ad_campaign_id, list_by_ad_unit_campaign, msg='对比相等，则用例通过')
        self.assertIn(new_ad_campaign_id1, list_by_ad_unit_campaign, msg='对比相等，则用例通过')
        '''撤销锁位'''
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


