import requests
import pymysql.cursors
import global_demo
import time
"""
周期管理模块的接口
@lihuanhuan@focusmedia.cn
"""


class AdCycleLock:
    @staticmethod
    def get_adcycle_lock_city():
        """
        检查当前城市是否有发布锁,使用批量查询接口查询
        :return: 返回有发布锁的周期的ID
        """
        get_city_lock = global_demo.GL_URL_AD_CYCLE + '/v1/adCycle/locks/batchLockQueryByCityAndDates'
        payload = {
             "items": [
                {
                    "cityId": global_demo.GL_CITY_ID,
                    "startDate": "2019-08-25",
                    "endDate": "2021-12-31"
                }
            ]
        }
        result = requests.post(get_city_lock, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        content = result.json()['items']
        adcycle_id_list = []
        for key in content:
            if len(key['locks']) == 0:
                return False
            else:
                for adcycle in key['locks']:
                    adcycle_id_list.append(adcycle['adCycle']['id'])
        return adcycle_id_list

    @staticmethod
    def put_adcycle_lock_city(ad_cycle_id):
        # 给城市加上发布锁
        put_city_lock = global_demo.GL_URL_AD_CYCLE + '/v1/adCycle/lock/'+global_demo.GL_CITY_ID+'/'+ad_cycle_id
        result = requests.post(put_city_lock, headers=global_demo.GL_HEADERS, verify=False)
        return result

    @staticmethod
    def delete_adcycle_lock_city(ad_cycle_id):
        # 解发布锁
        delete_city_lock = global_demo.GL_URL_AD_CYCLE + '/v1/adCycle/lock/'+global_demo.GL_CITY_ID+'/'+ad_cycle_id
        result = requests.delete(delete_city_lock, headers=global_demo.GL_HEADERS, verify=False)
        if result.status_code == 204:
            return True
        else:
            return False

    @staticmethod
    def delete_all_adcycle_lock():
        result = AdCycleLock().get_adcycle_lock_city()
        """
        如果获取城市发布锁的结果为false,直接返回
        如果获取城市发布锁的结果为true，删除发布锁，删除时对删除结果校验，删除成功继续，删除失败，返回false
        """
        if len(result)==0:
            return True
        else:
            for key in result:
                result = AdCycleLock().delete_adcycle_lock_city(key)
                if result:
                    continue
                else:
                    return False

            return True



# adCycleLock().delete_adcycle_lock_city('2019W42')