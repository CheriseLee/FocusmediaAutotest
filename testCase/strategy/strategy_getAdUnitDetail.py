import global_demo
import unittest
import time
import os
import ad_campaign
import ad_unit
import requests
"""
获取排播详情
@lihuanhuan@focusmedia.cn
"""


class TestCreateStrategy():
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_adunit_strategydetail(self):
        payload = {
            "adUnitId": "1010199132",
            "endDate": "2020-04-19",
            "invalid": False,
            "needKeyWordsTaboo": False,
            "startDate": "2020-04-13"
        }
        del_unit_url = global_demo.GL_URL_AD_STRATEGY + '/v1/getAdUnitStrategyDetail'
        result= requests.post(del_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # print(result.json())
        with open('detail.txt', 'w+') as write_f:
            write_f.write(str(result.json()))
        write_f.close()


if __name__ == '__main__':
    starttime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(starttime)
    TestCreateStrategy().get_adunit_strategydetail()
    endtime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(endtime)


