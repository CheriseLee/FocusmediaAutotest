import ad_unit
import unittest
import ad_campaign
import global_demo
import time_function
import pytest
import os

"""
创建单元
@lihuanhuan@focusmedia.cn
"""

class TestCreateUnit(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_create_guaranteed_building_unit1(self):
        '''创建必播/项目/待发布/tomorrow~nextnextsunday/15*300单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        ad_campaign_type = 'KA'
        ad_unit_type = 'GUARANTEED'
        start_date = time_function.GetTime.get_tomorrow()
        end_date = time_function.GetTime.get_next_next_sunday()
        ad_unit_target_ids = global_demo.GL_BUILDING_IDS
        target_type = 'BUILDING'
        goal_location_num = 10
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids, target_type,start_date,end_date,goal_location_num=goal_location_num)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["goalLocationNum"], goal_location_num, msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''必播项目挑点单元锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''撤销锁位'''
        revert_info = ad_unit.AdUnit().revert_unit(ad_unit_id)
        self.assertEqual(revert_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_unit(ad_unit_id)

    def test_create_guaranteed_city_unit2(self):
        '''创建必播/全城/发布中/today~tomorrow/15*900/模拟套装单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_tomorrow()
        frequency = 900
        goal_location_num = 10
        ad_campaign_type = 'KA'
        ad_unit_type = 'GUARANTEED'
        ad_unit_target_ids = global_demo.GL_CITY_ID
        target_type = 'CITY'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              goal_location_num=goal_location_num,frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["goalLocationNum"], goal_location_num, msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''必播项目挑点单元锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_guaranteed_building_unit3(self):
        '''创建必播/挑点/发布中/maxday~maxday/30*600单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_max_day()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 30
        frequency = 600
        goal_location_num = 10
        ad_campaign_type = 'KA'
        ad_unit_type = 'GUARANTEED'
        ad_unit_target_ids = global_demo.GL_BUILDING_IDS
        target_type = 'BUILDING'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,duration_in_second=duration_in_second,
                                                              goal_location_num=goal_location_num, frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["goalLocationNum"], goal_location_num, msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''必播项目挑点单元锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''终止单元'''
        revert_info = ad_unit.AdUnit().revert_unit(ad_unit_id)
        self.assertEqual(revert_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_guaranteed_suit_unit4(self):
            '''创建必播/套装/发布中/today~today/15*300单元'''
            global_demo.GL_DEL_CAMPAIGN_LIST = []
            '''创建单元'''
            start_date = time_function.GetTime.get_today()
            end_date = time_function.GetTime.get_tomorrow()
            ad_campaign_type = 'KA'
            ad_unit_type = 'GUARANTEED'
            ad_unit_target_ids = global_demo.GL_SUIT_CODES
            target_type = 'SUIT'
            create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                                  target_type, start_date, end_date)
            response = create_info.json()
            ad_unit_id = response["adUnitId"]
            ad_campaign_id = response["adCampaignId"]
            global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
            '''检查创建的单元信息和预期相同'''
            self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
            self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
            self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
            self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
            self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
            self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

            '''锁位'''
            reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
            reserve_response = reserve_info.json()
            self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

            '''终止单元'''
            terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
            self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
            '''删除单元'''
            ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_guaranteed_suit_unit5(self):
            '''创建必播/套装/发布中/today~maxday/5*50单元'''
            global_demo.GL_DEL_CAMPAIGN_LIST = []
            '''创建单元'''
            start_date = time_function.GetTime.get_today()
            end_date = time_function.GetTime.get_max_day()
            duration_in_second = 5
            frequency = 50
            ad_campaign_type = 'KA'
            ad_unit_type = 'GUARANTEED'
            ad_unit_target_ids = global_demo.GL_SUIT_CODES
            target_type = 'SUIT'
            create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                                  target_type, start_date, end_date,
                                                                  duration_in_second=duration_in_second,
                                                                  frequency=frequency)
            response = create_info.json()
            ad_unit_id = response["adUnitId"]
            ad_campaign_id = response["adCampaignId"]
            global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
            '''检查创建的单元信息和预期相同'''
            self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
            self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
            self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
            self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
            self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
            self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

            '''锁位'''
            reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
            reserve_response = reserve_info.json()
            self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

            '''终止单元'''
            terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
            self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
            '''删除单元'''
            ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)


    def test_create_guaranteed_city_hours_unit6(self):
        '''创建必播/全城/发布中/today~maxday/7.5*100/小时单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 7.5
        frequency = 100
        goal_location_num = 10
        ad_campaign_type = 'KA'
        ad_unit_type = 'GUARANTEED'
        ad_unit_target_ids = global_demo.GL_CITY_ID
        target_type = 'CITY'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              goal_location_num=goal_location_num, frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["goalLocationNum"], goal_location_num, msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''必播项目挑点单元锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    '''候补非抢占'''
    def test_create_vacant_candidate_suit_unit7(self):
        '''创建空位候补非抢占/套装/发布中/today~maxday/5*50单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 5
        frequency = 50
        ad_campaign_type = 'VACANT'
        ad_unit_type = 'CANDIDATE_NON_PREEMPTIVE'
        ad_unit_target_ids = global_demo.GL_SUIT_CODES
        target_type = 'SUIT'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE_NON_PREEMPTIVE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        reserve_info = ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_candidate_location_unit8(self):
        '''创建空位候补非抢占/项目/发布中/today~today/30*600单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_today()
        duration_in_second = 30
        frequency = 600
        goal_location_num = 10
        ad_campaign_type = 'VACANT'
        ad_unit_type = 'CANDIDATE_NON_PREEMPTIVE'
        ad_unit_target_ids = global_demo.GL_BUILDING_IDS
        target_type = 'BUILDING'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency,goal_location_num=goal_location_num)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE_NON_PREEMPTIVE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_candidate_city_unit9(self):
        '''创建空位候补非抢占/全城/发布中/today~maxday/15*300单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 15
        frequency = 300
        goal_location_num = 10
        ad_campaign_type = 'VACANT'
        ad_unit_type = 'CANDIDATE_NON_PREEMPTIVE'
        ad_unit_target_ids = global_demo.GL_CITY_ID
        target_type = 'CITY'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency, goal_location_num=goal_location_num)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE_NON_PREEMPTIVE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "SALE", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)


    '''候补可抢占'''
    def test_create_candidate_city_unit10(self):
        '''创建公益候补可抢占/全城模拟套装/发布中/today~maxday/5*50单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 5
        frequency = 50
        goal_location_num = 10
        ad_campaign_type = 'NONPROFIT'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_CITY_ID
        target_type = 'CITY'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency, goal_location_num=goal_location_num,fake_suit_info="A")
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "INSTALL", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_candidate_location_unit11(self):
        '''创建空位候补可抢占/项目/发布中/today~today/30*600单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_today()
        duration_in_second = 30
        frequency = 600
        goal_location_num = 10
        ad_campaign_type = 'VACANT'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_BUILDING_IDS
        target_type = 'BUILDING'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency, goal_location_num=goal_location_num)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "INSTALL", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_candidate_building_unit12(self):
        '''创建空位候补可抢占/按项目模拟套装/发布中/today~maxday/15*300单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 15
        frequency = 300
        goal_location_num = 10
        ad_campaign_type = 'VACANT'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_BUILDING_IDS
        target_type = 'BUILDING'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency, goal_location_num=goal_location_num,fake_suit_info="A")
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "INITIAL", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "INSTALL", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    '''物业单'''
    def test_create_guaranteed_building_unit13(self):
        '''创建全物管必播/发布中/today~maxday/15*300单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 15
        frequency = 300
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'GUARANTEED'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'PROPERTY_ADMIN'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "AUDITED", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "INSTALL", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_property_guaranteed_location_unit14(self):
        '''创建物管挑点必播/发布中/today~maxday/15*300单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 15
        frequency = 300
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'GUARANTEED'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'LOCATION'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "AUDITED", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "GUARANTEED", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "INSTALL", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        reserve_info = ad_unit.AdUnit().reserve_unit(ad_unit_id)
        reserve_response = reserve_info.json()
        self.assertTrue(reserve_response["success"],  msg='检查锁位成功，则用例通过')

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)

    def test_create_property_guaranteed_location_unit15(self):
        '''创建物管挑点候补可抢占/发布中/today~maxday/15*300单元'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_today()
        end_date = time_function.GetTime.get_max_day()
        duration_in_second = 15
        frequency = 300
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'LOCATION'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,
                                                              duration_in_second=duration_in_second,
                                                              frequency=frequency)
        response = create_info.json()
        ad_unit_id = response["adUnitId"]
        ad_campaign_id = response["adCampaignId"]
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(response["auditStatus"], "AUDITED", msg='对比相等，则用例通过')
        self.assertEqual(response["adUnitType"], "CANDIDATE", msg='对比相等，则用例通过')
        self.assertFalse(response["dsp"], msg='检查非DSP,则用例通过')
        self.assertEqual(response["adUnitStatus"], "PENDING", msg='对比相等，则用例通过')
        self.assertEqual(response["resourceAreaType"], "INSTALL", msg='对比相等，则用例通过')
        self.assertEqual(response["publishVersion"], 0, msg='对比相等，则用例通过')

        '''锁位'''
        ad_unit.AdUnit().confirm_unit(ad_unit_id)

        '''终止单元'''
        terminate_info = ad_unit.AdUnit().terminate_unit(ad_unit_id)
        self.assertEqual(terminate_info.status_code, 200, msg='对比相等，则用例通过')
        '''删除单元'''
        ad_unit.AdUnit().delete_CANDIDATE_unit_fromDB(ad_unit_id)


    '''异常场景'''
    def test_create_ka_guaranteed_location_unit16(self):
        '''创建昨天到今天的单元，创建失败'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_yesterday()
        end_date = time_function.GetTime.get_today()
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'LOCATION'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date)
        response = create_info.json()
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(create_info.status_code, 400, msg='对比相等，则用例通过')
        self.assertEqual(response["code"], "UnboundedRequestDate", msg='对比相等，则用例通过')

    def test_create_ka_guaranteed_location_unit17(self):
        '''创建最大日期以后的单元，创建失败'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_max_day()
        end_date = time_function.GetTime.get_bigger_than_max_day()
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'LOCATION'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date)
        response = create_info.json()
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(create_info.status_code, 400, msg='对比相等，则用例通过')
        self.assertEqual(response["code"], "UnboundedRequestDate", msg='对比相等，则用例通过')


    def test_create_ka_guaranteed_location_unit18(self):
        '''创建最大日期以后的单元，创建失败'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_max_day()
        end_date = time_function.GetTime.get_bigger_than_max_day()
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'LOCATION'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date)
        response = create_info.json()
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(create_info.status_code, 400, msg='对比相等，则用例通过')
        self.assertEqual(response["code"], "UnboundedRequestDate", msg='对比相等，则用例通过')

    def test_create_ka_guaranteed_location_unit19(self):
        '''创建所需点位数大于点位范围数的单元，创建失败'''
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建单元'''
        start_date = time_function.GetTime.get_next_monday()
        end_date = time_function.GetTime.get_next_monday()
        goal_location_num = 50000
        ad_campaign_type = 'PROPERTY'
        ad_unit_type = 'CANDIDATE'
        ad_unit_target_ids = global_demo.GL_PROPERTY_LOCATION_IDS
        target_type = 'LOCATION'
        create_info = ad_unit.AdUnit.create_campaign_and_unit(ad_campaign_type, ad_unit_type, ad_unit_target_ids,
                                                              target_type, start_date, end_date,goal_location_num=goal_location_num)
        response = create_info.json()
        '''检查创建的单元信息和预期相同'''
        self.assertEqual(create_info.status_code, 400, msg='对比相等，则用例通过')
        self.assertEqual(response["code"], "LocationIsNotEnough", msg='对比相等，则用例通过')

if __name__ == '__main__':

    pytest.main()