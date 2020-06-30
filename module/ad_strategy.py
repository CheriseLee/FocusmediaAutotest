import xlrd
import xlwt
import time_function
import requests
import global_demo
import ad_unit


class AdStrategy:
    @staticmethod
    def creative_Info_15():
        """配置15s排播的创意信息"""
        creative_info_15 = {
            "186073": "186073_C100828",
            "191738": "191738_C100620",
            "136730": "136730_C111002"
        }
        return creative_info_15

    @staticmethod
    def creative_Info_30():
        """配置30s排播的创意信息"""
        creative_info_30 = {
            "186073": "186073_C103805",
            "191738": "191738_C103806",
        }
        return creative_info_30

    @staticmethod
    def get_creative_id(duration, account_id, product_name):
        '''根据账号和单元时长查询匹配到的已审核创意'''
        payload = {
            "accountIds": [account_id],
            "groupDurations": [duration],
            "groupFilters": [
                {
                    "keyword": "STATUS",
                    "values": [
                        "AUDIT_PASS"
                    ]
                },
                {
                    "keyword": "SOURCE",
                    "values": [
                        "MANAGEMENT"
                    ]
                }
            ],
            "productName": product_name
        }
        get_creative_url = global_demo.GL_URL_AD_CREATIVE + '/v1/creative-group/list'
        result = requests.post(get_creative_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json().get('data')  # 获取创意列表

        # print(type(response))
        creative_id_list = []
        for key, value in enumerate(response):
            creative_id_list.append(value.get('creativeGroupId'))

        return creative_id_list

    @staticmethod
    def create_AdUnitStrategy(ad_unit_id):
        '''获取单元信息，进行单元级别的排播'''
        unit_info = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        start_date = unit_info['startDate']
        end_date = unit_info['endDate']
        duration = unit_info['durationInSecond']
        report_id = unit_info['referId']
        creative_group_id = AdStrategy.get_creative_id(duration, report_id)
        payload = {
            "adUnitId": str(ad_unit_id),
            "creativeGroupIds": creative_group_id,
            "startDate": start_date,
            "startTime": "00:00:00",
            "endDate": end_date,
            "endTime": "23:59:59"
        }

        create_strategy = global_demo.GL_URL_AD_STRATEGY + '/v1/createAdUnitStrategy'
        requests.post(create_strategy, json=payload, headers=global_demo.GL_HEADERS, verify=False)

    @staticmethod
    def getAdUnitsWithCreativeTaboo(start_date,end_date,product_name):
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "productName": product_name
        }
        create_campaign = global_demo.GL_URL_AD_STRATEGY + '/v1/getAdUnitsWithCreativeTaboo'
        result = requests.post(create_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result



if __name__ == '__main__':

        AdStrategy.create_AdUnitStrategy('1010182686')
