import time
import pytest
import ad_campaign
import global_demo
import ad_unit

"""
批量创建单元
@lihuanhuan@focusmedia.cn
"""


class TestBatchCreateAdUnits():
    def setup_method(self):
        pass

    def teardown_method(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_create_ad_units(self):
        '''批量创建单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        ''' 创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_type, campaign_name)
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        result = ad_unit.AdUnit.batch_create_adunits(ad_campaign_id, unit_no=3, goal_location_num=10)

        '''检查创建的单元信息和预期相同'''
        assert result.status_code == 200
        ad_unit_ids = result.json()
        print(type(ad_unit_ids))
        ad_unit.AdUnit.batch_delete_adunits(ad_unit_ids)

    def test_batch_create_ad_unit(self):
        '''批量创建单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        ''' 创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_type, campaign_name)
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        ad_unit_ids =  ad_unit.AdUnit.batch_create_adunits(ad_campaign_id)
        print(type(ad_unit_ids))
        ad_unit.AdUnit.batch_delete_adunits(ad_unit_ids)



if __name__ == '__main__':
    # pytest.main(["test_batch_create_ad_units.py::TestBatchCreateAdUnits::test_create_ad_units"])
    # pytest.main(["test_batch_create_ad_units.py"])
    TestBatchCreateAdUnits().test_create_ad_units()

