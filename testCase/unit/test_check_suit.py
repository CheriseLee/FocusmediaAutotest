import time_function
import pytest
import ad_campaign
import global_demo
import ad_unit

"""
检查套装在哪些单元中用到
@lihuanhuan@focusmedia.cn
"""


class TestCheckSuit():
    def setup_method(self):
        pass

    def teardown_method(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_check_suit(self):
        '''检查套装被哪些单元使用'''
        start_date = time_function.GetTime.get_next_monday()
        city_id=global_demo.GL_CITY_ID
        suit_code = global_demo.GL_SUIT_CODES
        ad_unit_ids =  ad_unit.AdUnit.check_suit(start_date,city_id,suit_code)



if __name__ == '__main__':
    pytest.main(["test_check_suit.py"])

