import requests
import global_demo

"""
计划模块的接口
@lihuanhuan@focusmedia.cn
"""


class AdCampaign:
    @staticmethod
    def del_campaign(ad_campaign_id):
        """
        删除计划，如果计划下存在单元（DELETE状态除外），删除失败
        :param ad_campaign_id:
        :return: 删除请求的返回值
        """
        del_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/delete/' + ad_campaign_id
        result = requests.post(del_campaign, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_campaign(refer_id, campaign_type, campaign_name, note=''):
        """
        创建一个计划
        :param refer_id:
        :param campaign_name:
        :param campaign_type:
        :param note:
        :return:
        """
        payload = {
            "referId": refer_id,
            "adCampaignName": campaign_name,
            "adCampaignType": campaign_type,
            "productName": "SMART_SCREEN",
            "source": "CONSOLE",
            "note": note
        }
        # print(payload)
        create_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/create'
        result = requests.post(create_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def edit_campaign(ad_campaign_id, campaign_name, note):
        '''修改一个计划'''
        payload = {
            "adCampaignId": ad_campaign_id,
            "adCampaignName": campaign_name,
            "note": note
        }
        edit_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/edit'
        result = requests.post(edit_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def audit_campaign(ad_campaign_id, contract_no, contract_type,brand, industry, pb_content, audit_type):
        """
        审核计划，计划下有意向中单元时，审核失败
        :param ad_campaign_id:
        :return:
        """
        payload = {
            "adCampaignId": ad_campaign_id,
            "contractNo": contract_no,
            "brand": brand,
            "industry": industry,
            "contractType": contract_type,
            "pbContent": pb_content,
            "auditType": audit_type
        }
        audit_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/auditAndBindContract'
        result = requests.post(audit_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def lock_campaign(ad_campaign_id):
        # 锁定计划
        lock_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/lock/' + ad_campaign_id
        result = requests.post(lock_campaign, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def unlock_campaign(ad_campaign_id):
        '''解锁计划'''
        unlock_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/unLock/' + ad_campaign_id
        result = requests.post(unlock_campaign, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def list_campaign():
        """
        查询最近的n个计划
        :return: 查询到的计划列表
        """
        n = 10
        payload = {
                # "adCampaignIdList": ad_campaign_id_list,
                # "referIdList": '',
                # "adCampaignTypeList": '',
                # "contractNoList": '',
                # "auditStatusList": '',
                # "adCampaignName": '',
                # "note": '',
                # "brand": '',
                "pageNo": 1,
                "pageSize": n,
                "source": "CONSOLE"
                # "orderByCreateTime": '',
                # "orderByAdUnitCount": ''
        }
        list_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/list'
        result = requests.post(list_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        content = result.json()['result']
        ad_campaign_list = []
        for key in content:
            ad_campaign_list.append(key['adCampaignId'])

        return ad_campaign_list

    @staticmethod
    def search_campaign_info(ad_campaign_id):
        """
        查询一个计划的详细信息
        :return: 计划的详细信息
        """
        n = 10
        payload = {
                "adCampaignIdList": ad_campaign_id,
                # "referIdList": '',
                # "adCampaignTypeList": '',
                # "contractNoList": '',
                # "auditStatusList": '',
                # "adCampaignName": '',
                # "note": '',
                # "brand": '',
                "pageNo": 1,
                "pageSize": n,
                # "orderByCreateTime": '',
                # "orderByAdUnitCount": ''
        }
        list_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/list'
        result = requests.post(list_campaign, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        content = result.json()['result'][0]
        return content

    @staticmethod
    def unaudit_campaign_list(start_date, end_date, initial_reserved, urgent_expired):
        """
        查询锁位未审核、急播过期计划
        :param startdate:
        :param enddate:
        :param initial_reserved:
        :param urgent_expired:
        :return: 返回查询到的计划列表
        """
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            # "cityId": "null",
            "initialReserved": initial_reserved,
            "urgentExpired": urgent_expired,
            "productName": "SMART_SCREEN",
            "pageNo": 1,
            "pageSize": 1000
        }
        campaign_info_list = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/listByAdUnit'
        response = requests.post(campaign_info_list, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        campaign_info_list = response.json()['result']

        campaign_id_list = []
        for key in campaign_info_list:
            campaign_id_list.append(key['adCampaignId'])
        return campaign_id_list




