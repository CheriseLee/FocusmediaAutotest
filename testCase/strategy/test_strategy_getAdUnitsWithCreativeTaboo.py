import global_demo
import time
import requests
import pytest
import time_function
"""
创建目标级别的排播getAdUnitsWithCreativeTaboo
@lihuanhuan@focusmedia.cn
"""


class TestGetAdUnitsWithCreativeTaboo():
    @pytest.fixture()
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

    def test_get_adUnits_with_creative_taboo(self):
        payload = {
            "startDate": time_function.GetTime.get_this_monday(),
            "endDate": time_function.GetTime.get_this_sunday(),
            "productName": "SMART_SCREEN"
        }
        create_campaign = global_demo.GL_URL_AD_STRATEGY + '/v1/getAdUnitsWithCreativeTaboo'
        result = requests.post(create_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

if __name__ == '__main__':
    starttime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(starttime)
    pytest.main()
    endtime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(endtime)



