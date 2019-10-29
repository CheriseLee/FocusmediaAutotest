import ad_unit
import unittest
import ad_campaign
import global_demo
import time_function
import time

"""
创建单元
@lihuanhuan@focusmedia.cn
"""

class CreateUnit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    '''无锁，创建单元'''
    def test_create_candidate_dsp_location_unit(self):
        '''创建候补可抢占、程序化、挑点单'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        ''' 创建一个计划'''
        refer_id = '136381'
        campaign_type = 'KA'
        campaign_name = time.strftime("%Y-%m-%d %H_%M_%S")
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)
        '''创建单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        duration_in_second = 30
        frequency = 100
        start_date = tomorrow
        end_date = tomorrow
        ad_unit_type = 'CANDIDATE'
        dsp = True
        suit_codes = ['EA300101']
        ad_campaign_id = ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'LOCATION'
        ad_unit_id_info = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type,
                                                  dsp, suit_codes, ad_campaign_id, dsp_id, target_type)
        print(ad_unit_id_info)
        ad_unit_id = ad_unit_id_info['adUnitId']

        # self.assertEqual(result.status_code, 200, msg='审核计划失败，状态码为200')
        # self.assertEqual(content['success'], False, msg='审核计划失败，审核成功状态值为false 则用例通过')
        ad_unit.AdUnit.delete_unit(ad_unit_id)
