import global_demo
import requests
import unittest
import time



class createCampaign(unittest.TestCase):
    def setUp(self):
        print("start test")

    def tearDown(self):
        for key in (global_demo.GL_delCampaignList):
            payload = {}
            delCampaign = global_demo.GL_baseURL_ad_Group + '/v1/ad/campaign/delete/' + key
            result = requests.post(delCampaign, json=payload, headers=global_demo.GL_headers, verify=False)
        print("end test")
    def test_createCampaign_normal(self):
        del_campaign_list = []
        # 报告命名时间格式化
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        payload = {
            "referId": "136381",
            "adCampaignName": "lihhtest"+now,
            "adCampaignType": "VACANT",
            "note": "121"
        }
        createCampaign = global_demo.GL_baseURL_ad_Group + '/v1/ad/campaign/create'
        result = requests.post(createCampaign, json=payload, headers=global_demo.GL_headers, verify=False)
        print(result.text)
        global_demo.GL_delCampaignList.append(result.text)

if __name__ == '__main__':
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(createCampaign("test_createCampaign_normal"))
    print(suite)
    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)


