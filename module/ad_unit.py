import requests
import global_demo
import time
import ad_campaign
import time_function
import ad_resource
import json
"""
单元模块的接口
@lihuanhuan@focusmedia.cn
"""


class AdUnit:

    @staticmethod
    def insert_CANDIDATE_unit_toDB(ad_campaign_id, ad_unit_status):
        '''向数据库里插入一条候补单'''
        cursor = global_demo.GL_CONNECTION.cursor()
        ad_unit_id = time.strftime("%Y-%m-%d %H_%M_%S")
        '''创建sql 语句'''
        sql = "INSERT INTO `kuma_ad_group`.`ad_unit`(" \
              "`ad_unit_id`, `ad_unit_type`, `ad_unit_status`, `city_id`, `start_date`, `end_date`,`duration_in_second`, `frequency`, `target_type`, `target_count`, `goal_location_num`, `ad_campaign_id`) " \
              " VALUES(%(ad_unit_id)s, %(ad_unit_type)s, %(ad_unit_status)s, %(city_id)s, %(start_date)s, %(end_date)s, %(duration_in_second)r, %(frequency)r, %(target_type)s, %(target_count)r, %(goal_location_num)r,%(ad_campaign_id)s)"
        startdate = time_function.GetTime.get_this_sunday()
        enddate = time_function.GetTime.get_next_next_monday()
        value = {
            "ad_unit_id": ad_unit_id,
            "ad_unit_type": "CANDIDATE",
            "ad_unit_status": ad_unit_status,
            "city_id": "110000000000",
            "start_date": startdate,
            "end_date": enddate,
            "duration_in_second": 15,
            "frequency": 300,
            "target_type": "CITY",
            "target_count": 30,
            "goal_location_num": 10,
            "ad_campaign_id": ad_campaign_id
        }
        '''执行sql语句，避免sql执行失败产生死锁'''
        try:
            cursor.execute(sql, value)
            global_demo.GL_CONNECTION.commit()
        except Exception as e:
            global_demo.GL_CONNECTION.rollback()
        return ad_unit_id

    @staticmethod
    def delete_CANDIDATE_unit_fromDB(ad_unit_id):
        '''从数据库里删除一条候补单'''
        cursor = global_demo.GL_CONNECTION.cursor()
        '''创建sql 语句'''
        sql = "DELETE FROM ad_unit WHERE ad_unit_id = '%s'"%ad_unit_id

        '''执行sql语句，避免sql执行失败产生死锁'''
        try:
            cursor.execute(sql)
            global_demo.GL_CONNECTION.commit()
        except Exception as e:
            global_demo.GL_CONNECTION.rollback()
        return ad_unit_id

    @staticmethod
    def batch_create_adunits(ad_campaign_id, unit_no, goal_location_num):
        """批量创建单元，只能针对同一个计划创建"""
        #获取全部城市ID
        city_id_list = ad_resource.AdResource.get_all_city_id()

        ad_unit_items = []
        for i in range(unit_no):
            item ={}
            item['cityId'] = city_id_list[i]
            item['goalLocationNum'] = goal_location_num
            item['scopeEnum'] = "ALL"
            item['targetIds'] = city_id_list[i]
            item['targetType'] = "CITY"
            ad_unit_items.append(item)

        payload = {
            "adCampaignId": ad_campaign_id,
            "adUnitItemRequests": ad_unit_items,
            "adUnitType": "GUARANTEED",
            "durationInSecond": "15",
            "frequency": "300",
            "startDate": time_function.GetTime.get_next_monday(),
            "endDate": time_function.GetTime.get_next_sunday(),
            "hours": [],
            "dsp": False
        }
        batchCreateAdUnits = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/batchCreateAdUnits'
        result = requests.post(batchCreateAdUnits,json=payload, headers=global_demo.GL_HEADERS, verify=False)

        return result

    @staticmethod
    def batch_delete_adunits(ad_unit_ids):
        """批量删除单元"""
        payload=[str(ad_unit_ids)]
        # payload =json.dumps(ad_unit_ids)

        batchdeleteAdUnits = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/batchDelete'
        result = requests.post(batchdeleteAdUnits,data=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result.json()

    @staticmethod
    def cancel_unit(ad_unit_id):
        """取消单元"""
        payload = {
            "adUnitId": ad_unit_id
        }
        terminate_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/cancel/'+ad_unit_id
        result = requests.post(terminate_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def check_suit(start_date,city_id,suit_code):
        """检查套装在哪些单元中使用"""
        payload = {
              "startDate": start_date,
                   "suitInfo": {
                   "cityId": city_id,
                   "suitCode": suit_code[0]
              }
        }
        check_suit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/checkSuit'
        result = requests.post(check_suit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def confirm_unit(ad_unit_id):
        """单元确认"""
        payload = {
            "adUnitId": ad_unit_id
        }
        confirm_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/confirm/' + ad_unit_id
        result = requests.post(confirm_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_pure_unit(ad_campaign_id,ad_unit_type, ad_unit_target_ids, target_type, start_date=time_function.GetTime.get_tomorrow(),
                         end_date=time_function.GetTime.get_next_next_sunday(), duration_in_second=15, frequency=300,
                         dsp=False,  dsp_id='', hours=[], fake_suit_info="", goal_location_num=1):

        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "goalLocationNum": goal_location_num,
            # "productName": "SMART_SCREEN",
            "adUnitType": ad_unit_type,
            "dsp": dsp,
            "adUnitTargetIds": ad_unit_target_ids,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "dspId": dsp_id,
            "targetType": target_type,
            "fakeSuitInfo":fake_suit_info
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # response = result.json()
        # ad_unit_id = response['adUnitId']
        return result

    @staticmethod
    def create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids, target_type, start_date=time_function.GetTime.get_tomorrow(),
                         end_date=time_function.GetTime.get_next_next_sunday(), duration_in_second=15, frequency=300,
                         dsp=False,  dsp_id='', hours=[], fake_suit_info="", goal_location_num=1):

        if ad_campaign_type == 'KA' or ad_campaign_type == 'VACANT':
            refer_id = global_demo.GL_REFER_ID1
        elif ad_campaign_type == 'NONPROFIT':
            refer_id = global_demo.GL_NONPROFIT_ID
        elif ad_campaign_type == 'PROPERTY':
            refer_id = global_demo.GL_PROPERTY_ADMINID

        result = ad_campaign.AdCampaign.create_campaign(refer_id, ad_campaign_type, campaign_name=int(round(time.time() * 1000000)), note='')
        ad_campaign_id = result.text

        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "goalLocationNum": goal_location_num,
            # "productName": "SMART_SCREEN",
            "adUnitType": ad_unit_type,
            "dsp": dsp,
            "adUnitTargetIds": ad_unit_target_ids,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "dspId": dsp_id,
            "targetType": target_type,
            "fakeSuitInfo":fake_suit_info
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # response = result.json()
        # ad_unit_id = response['adUnitId']
        return result

    @staticmethod
    def edit_unit(ad_unit_id, duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, ad_unit_target_ids, ad_campaign_id, dsp_id, target_type, hours=[],fakeSuitInfo="",goal_location_num = 1):
        '''修改意向中单元'''
        payload = {
            "adUnitId": ad_unit_id,
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "goalLocationNum": goal_location_num,
            "adUnitType": ad_unit_type,
            "dsp": dsp,
            "adUnitTargetIds": ad_unit_target_ids,
            "cityId": global_demo.GL_CITY_ID,
            "dspId": dsp_id,
            "targetType": target_type,
            "fakeSuitInfo":fakeSuitInfo
        }
        edit_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/edit'
        result = requests.post(edit_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # response = result.json()
        # ad_unit_id = response['adUnitId']
        return result

    @staticmethod
    def reserve_unit(ad_unit_id):
        """单元锁位"""
        payload = {
            "adUnitId": ad_unit_id
        }
        reserve_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/reserve'
        result = requests.post(reserve_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result



    @staticmethod
    def revert_unit(ad_unit_id):
        """撤销锁位"""
        revert_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/revert/' + ad_unit_id
        result = requests.post(revert_unit, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def delete_unit(ad_unit_id):
        """删除单元"""
        '''查询单元状态，如果是意向中则删除，其他状态返回False'''
        result = AdUnit.get_unit_info(ad_unit_id)
        unit_status = result['adUnitStatus']
        if unit_status == 'PENDING':
            payload = [ad_unit_id]
            delete_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/batchDelete'
            result = requests.post(delete_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
            if result.status_code == 200:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def terminate_unit(ad_unit_id):
        """终止单元"""
        payload = {
            "adUnitId": ad_unit_id
        }
        terminate_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/terminate'
        result = requests.post(terminate_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result



    @staticmethod
    def get_unit_info(ad_unit_id):
        """获取单元详情"""
        get_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/get/' + ad_unit_id
        result = requests.get(get_unit, headers=global_demo.GL_HEADERS, verify=False)
        return result.json()

    @staticmethod
    def get_unit_list(page_no, page_size, ad_campaign_id_list, ad_unit_status_list=None,city_id_list=None,
                      start_date=None, end_date=None, product_name='SMART_SCREEN'):
        """获取投放单元列表"""
        payload = {
            "adCampaignIdList": ad_campaign_id_list,
            "adUnitStatusList": ad_unit_status_list,
            "cityIdList": city_id_list,
            "startDate": start_date,
            "endDate": end_date,
            "pageNo": page_no,
            "pageSize": page_size,
            "productName": product_name
        }
        get_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/list'
        result = requests.post(get_unit,json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result.json()

