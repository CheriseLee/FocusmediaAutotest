import ad_unit
import unittest
import ad_campaign
import global_demo
import time_function
import time
import pytest

"""
编辑意向中单元
@lihuanhuan@focusmedia.cn
"""


class TestEditUnit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_edit_unit(self):
        '''单元状态为意向中，编辑单元'''

        global_demo.GL_DEL_CAMPAIGN_LIST = []
        ''' 创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text

        '''创建单元'''
        start_date = time_function.GetTime.get_tomorrow()
        end_date = time_function.GetTime.get_next_next_sunday()
        duration_in_second=15
        frequency=300
        ad_unit_type='GUARANTEED'
        dsp = False
        ad_unit_target_ids = global_demo.GL_SUIT_CODES
        dsp_id=''
        target_type='SUIT'
        create_info = ad_unit.AdUnit.create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, ad_unit_target_ids, ad_campaign_id, dsp_id, target_type, hours=[],fakeSuitInfo="",goal_location_num = 1)

        '''编辑单元'''


if __name__ == '__main__':
    pytest.main(["test_unit_edit.py"])