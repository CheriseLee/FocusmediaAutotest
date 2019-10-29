import requests
import global_demo
import time
import ad_cycle
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
        nowdate = time.strftime("%Y-%m-%d")
        value = {
            "ad_unit_id": ad_unit_id,
            "ad_unit_type": "CANDIDATE",
            "ad_unit_status": ad_unit_status,
            "city_id": "110000000000",
            "start_date": nowdate,
            "end_date": nowdate,
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
            global_demo.connection.commit()
        except Exception as e:
            global_demo.connection.rollback()
        return ad_unit_id

    @staticmethod
    def delete_CANDIDATE_unit_fromDB(ad_unit_id):
        '''从数据库里删除一条候补单'''
        cursor = global_demo.GL_CONNECTION.cursor()
        '''创建sql 语句'''
        sql = "DELETE FROM ad_unit WHERE ad_unit = %s"%ad_unit_id

        '''执行sql语句，避免sql执行失败产生死锁'''
        try:
            cursor.execute(sql)
            global_demo.connection.commit()
        except Exception as e:
            global_demo.connection.rollback()
        return ad_unit_id

    @staticmethod
    def create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type, dsp, suit_codes, ad_campaign_id, dsp_id, target_type):
        """ 1.创建单元;2.删除当前城市所有发布锁,删除成功，则创建单元"""
        result = ad_cycle.AdCycleLock.delete_all_adcycle_lock()
        if result:
            payload = {
                "durationInSecond": duration_in_second,
                "frequency": frequency,
                "startDate": start_date,
                "endDate": end_date,
                "hours": [
                    12,
                    11
                ],
                # "goalLocationNum": 2,
                # "productName": "SMART_SCREEN",
                "adUnitType": ad_unit_type,
                "dsp": dsp,
                # "buildingIds": 'null',
                # "locationIds": 'null',
                "suitCodes": suit_codes,
                "adCampaignId": ad_campaign_id,
                "cityId": global_demo.GL_CITY_ID,
                "dspId": dsp_id,
                "targetType": target_type
            }
            create_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
            result = requests.post(create_unit, json=payload, headers=global_demo.GL_HEADERS, verify=False)
            response = result.json()
            # ad_unit_id = response['adUnitId']
            return response

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

            "token 取不到,无法从接口删除单元，暂时从数据库直接删"
        #     # 通过cursor创建游标
        #     cursor = global_demo.GL_CONNECTION.cursor()
        #     sql = "DELETE FROM `kuma_ad_group`.`ad_unit` WHERE ad_unit_id='%s'"%ad_unit_id
        #     '''执行sql语句，避免sql执行失败产生死锁'''
        #     try:
        #         cursor.execute(sql)
        #         global_demo.connection.commit()
        #         return True
        #     except Exception as e:
        #         global_demo.connection.rollback()
        #         return False
        # else:
        #     return False

    @staticmethod
    def get_unit_info(ad_unit_id):
        get_unit = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/get/' + ad_unit_id
        result = requests.get(get_unit, headers=global_demo.GL_HEADERS, verify=False)
        return result.json()



# AdUnit.delete_unit('2019-10-12 17_26_11')