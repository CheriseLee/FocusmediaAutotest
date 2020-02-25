import requests
import global_demo
import time
import ad_campaign
import time_function
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
            global_demo
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
    def create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, ad_unit_target_ids, ad_campaign_id, dsp_id, target_type, hours=[],fakeSuitInfo="",goal_location_num = 1):

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
            "fakeSuitInfo":fakeSuitInfo
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # response = result.json()
        # ad_unit_id = response['adUnitId']
        return result


    @staticmethod
    def create_ka_guaranteed_suit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建KA必播套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "targetType": "SUIT",
            "adUnitTargetIds": global_demo.GL_SUIT_CODES,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result


    @staticmethod
    def create_ka_guaranteed_building_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建KA必播按项目下单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "targetType": "BUILDING",
            "adUnitTargetIds": global_demo.GL_BUILDING_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result


    @staticmethod
    def create_ka_guaranteed_city_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建KA必播全城单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_ka_guaranteed_city_fakesuit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建KA必播全城模拟套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num,
            "fakeSuitInfo": "A"
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_ka_guaranteed_building_fakesuit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建KA必播按项目下模拟套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "targetType": "BUILDING",
            "adUnitTargetIds": global_demo.GL_BUILDING_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num,
            "fakeSuitInfo": "A"
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_ka_candidate_suit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[], goal_location_num=-1):

        ''' 创建一个计划，创建KA候补套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE",
            "targetType": "SUIT",
            "adUnitTargetIds": global_demo.GL_SUIT_CODES,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_ka_non_candidate_building_unit(start_date=time_function.GetTime.get_tomorrow(),
                                           end_date=time_function.GetTime.get_next_next_sunday(),
                                           duration_in_second=15,
                                           frequency=300,
                                           hours=[], goal_location_num=-1):

        ''' 创建一个计划，创建KA候补非抢占按项目下单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='KA', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE_NON_PREEMPTIVE",
            "targetType": "BUILDING",
            "adUnitTargetIds": global_demo.GL_BUILDING_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result


    '''创建候补单'''
    @staticmethod
    def create_vacant_non_candidate_city_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建空位候补非抢占全城单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID2,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='VACANT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE_NON_PREEMPTIVE",
            "targetType": "CITY",
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_vacant_non_candidate_suit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建空位候补非抢占套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID2,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='VACANT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE_NON_PREEMPTIVE",
            "targetType": "SUIT",
            "adUnitTargetIds": global_demo.GL_SUIT_CODES,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_vacant_non_candidate_building_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建空位候补非抢占挑点单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID2,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='VACANT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE_NON_PREEMPTIVE",
            "targetType": "BUILDING",
            "adUnitTargetIds": global_demo.GL_BUILDING_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result
    @staticmethod
    def create_vacant_candidate_building_unit(start_date=time_function.GetTime.get_tomorrow(),
                                           end_date=time_function.GetTime.get_next_next_sunday(),
                                           duration_in_second=15,
                                           frequency=300,
                                           hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建空位候补可抢占按项目下单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='VACANT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE",
            "targetType": "BUILDING",
            "adUnitTargetIds": global_demo.GL_BUILDING_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result


    @staticmethod
    def create_vacant_candidate_building_fakesuit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                                    end_date=time_function.GetTime.get_next_next_sunday(),
                                                    duration_in_second=15,
                                                    frequency=300,
                                                    hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建空位候补按项目下模拟套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='VACANT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE",
            "targetType": "BUILDING",
            "adUnitTargetIds": global_demo.GL_BUILDING_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num,
            "fakeSuitInfo": "A"
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_nonprofit_non_candidate_city_unit(start_date=time_function.GetTime.get_tomorrow(),
                                       end_date=time_function.GetTime.get_next_next_sunday(),
                                       duration_in_second=15,
                                       frequency=300,
                                       hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建公益候补非抢占全城单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_REFER_ID1,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='NONPROFIT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE_NON_PREEMPTIVE",
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_nonprofit_candidate_city_fakesuit_unit(start_date=time_function.GetTime.get_tomorrow(),
                                                end_date=time_function.GetTime.get_next_next_sunday(),
                                                duration_in_second=15,
                                                frequency=300,
                                                hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建公益候补全城模拟套装单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_NONPROFIT_ID,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='NONPROFIT', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE",
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num,
            "fakeSuitInfo": "A"
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_property_location_guaranteed_unit(start_date=time_function.GetTime.get_tomorrow(),
                                                      end_date=time_function.GetTime.get_next_next_sunday(),
                                                      duration_in_second=15,
                                                      frequency=300,
                                                      hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建物业必播挑点单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_PROPERTY_ADMINID,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='PROPERTY', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "targetType": "LOCATION",
            "adUnitTargetIds": global_demo.GL_PROPERTY_LOCATION_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num,
            "fakeSuitInfo": "A"
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result


    @staticmethod
    def create_property_total_guaranteed_unit(start_date=time_function.GetTime.get_tomorrow(),
                                                      end_date=time_function.GetTime.get_next_next_sunday(),
                                                      duration_in_second=15,
                                                      frequency=300,
                                                      hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建物业必播全物管单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_PROPERTY_ADMINID,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='PROPERTY', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "GUARANTEED",
            "targetType": "PROPERTY_ADMIN",
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def create_property_candidate_unit(start_date=time_function.GetTime.get_tomorrow(),
                                                      end_date=time_function.GetTime.get_next_next_sunday(),
                                                      duration_in_second=15,
                                                      frequency=300,
                                                      hours=[],goal_location_num=-1):

        ''' 创建一个计划，创建物业候补挑点单 '''
        result = ad_campaign.AdCampaign.create_campaign(refer_id=global_demo.GL_PROPERTY_ADMINID,
                                                        campaign_name=int(round(time.time() * 1000000)),
                                                        campaign_type='PROPERTY', note='')
        ad_campaign_id = result.text
        '''创建单元的请求参数'''
        payload = {
            "durationInSecond": duration_in_second,
            "frequency": frequency,
            "startDate": start_date,
            "endDate": end_date,
            "hours": hours,
            "adUnitType": "CANDIDATE",
            "targetType": "LOCATION",
            "adUnitTargetIds": global_demo.GL_PROPERTY_LOCATION_IDS,
            "adCampaignId": ad_campaign_id,
            "cityId": global_demo.GL_CITY_ID,
            "goalLocationNum": goal_location_num
        }
        create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
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
    def confirm_unit(ad_unit_id):
        """单元确认"""
        payload = {
            "adUnitId": ad_unit_id
        }
        confirm_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/confirm/' + ad_unit_id
        result = requests.post(confirm_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
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
    def cancel_unit(ad_unit_id):
        """取消单元"""
        payload = {
            "adUnitId": ad_unit_id
        }
        terminate_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/cancel/'+ad_unit_id
        result = requests.post(terminate_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def get_unit_info(ad_unit_id):
        get_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/get/' + ad_unit_id
        result = requests.get(get_unit, headers=global_demo.GL_HEADERS, verify=False)
        return result.json()


# AdUnit.create_unit(duration_in_second=30, frequency=100, start_date='2019-12-12', end_date='2019-12-12', ad_unit_type='CANDIDATE',
#                                                   dsp=True, suit_codes=['EA300101'], ad_campaign_id='186073_123039', dsp_id=global_demo.GL_DSPID1, target_type='LOCATION')
# AdUnit.create_ka_guaranteed_building_unit()