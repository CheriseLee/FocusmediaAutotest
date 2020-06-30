import global_demo
import unittest
import time
import os
import ad_campaign
import ad_unit
import time_function
import pytest
"""
审核计划，计划下有意向中单元时，审核失败
@lihuanhuan@focusmedia.cn
"""


class TestAuditCampaign(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        for ad_campaign_id in global_demo.GL_DEL_CAMPAIGN_LIST:
            ad_campaign.AdCampaign().del_campaign(ad_campaign_id)

    def test_audit_campaign_success(self):
        """ 计划下无任何单元，审核为合同号，审核成功"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id = global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text

        '''审核计划'''
        contract_no = '12345678901234567890123456789012'
        contract_type = 'CONTRACT'
        result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
        content = result.json()
        self.assertEqual(result.status_code, 200, msg='审核计划成功，状态码为200则用例通过')
        self.assertEqual(content['success'], True, msg='审核计划成功，审核成功状态值为true 则用例通过')
        '''检查接口返回信息和创建信息相同'''
        result = ad_campaign.AdCampaign.search_campaign_info(ad_campaign_id)
        self.assertEqual(result['contractNo'], contract_no, msg='检查合同号，相同则用例通过')
        self.assertEqual(result['contractType'], contract_type, msg='检查计划审核类型，相同则用例通过')
        self.assertEqual(result['auditStatus'], 'AUDITED', msg='检查计划已审核，相同则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

    def test_audit_urgent_campaign_success(self):
        """ 计划下无任何单元，审核为急播单号，审核成功，检查过期日期为下周日"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        ''' 创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text

        '''审核计划'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
        content = result.json()
        self.assertEqual(result.status_code, 200, msg='审核计划成功，状态码为200则用例通过')
        self.assertEqual(content['success'], True, msg='审核计划成功，审核成功状态值为true 则用例通过')
        '''检查接口返回信息和创建信息相同'''
        result = ad_campaign.AdCampaign.search_campaign_info(ad_campaign_id)
        self.assertEqual(result['contractNo'], contract_no, msg='检查计划ID，相同则用例通过')
        self.assertEqual(result['contractType'], contract_type, msg='检查计划名称，相同则用例通过')
        self.assertEqual(result['auditStatus'], 'AUDITED', msg='检查计划已审核，相同则用例通过')
        next_sunday = time_function.GetTime.get_next_sunday()
        self.assertEqual(result['urgentExpireDate'], next_sunday, msg='检查急播过期时间为下周日，相同则用例通过')
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

    def test_audit_wait_campaign_success(self):
        """计划下有WAIT、SHOW、CANCELLED、FINISH、TERMINATED状态的单元，可以审核"""
        unit_status_list = ['WAIT', 'SHOW', 'CANCELLED', 'FINISH', 'TERMINATED']
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        for unit_status in unit_status_list:
            '''创建一个计划'''
            refer_id=global_demo.GL_REFER_ID1
            campaign_type = 'KA'
            campaign_name = int(round(time.time() * 1000000))
            result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
            ad_campaign_id = result.text
            global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
            time.sleep(1)

            '''在计划下插入一个候补单元'''
            ad_unit_id = ad_unit.AdUnit.insert_CANDIDATE_unit_toDB(ad_campaign_id, unit_status)
            '''审核计划,审核成功'''
            contract_no = 'contract_no'
            contract_type = 'URGENT'
            result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
            content = result.json()
            self.assertEqual(result.status_code, 200, msg='审核计划成功，状态码为200')
            self.assertEqual(content['success'], True, msg='审核计划成功，审核成功状态值为true 则用例通过')
            '''删除插入的候补单元'''
            ad_unit.AdUnit.delete_CANDIDATE_unit_fromDB(ad_unit_id)


    def test_audit_pending_campaign_fail(self):
        """计划下有意向中单元，审核失败"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        ''' 创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下创建一个意向中的必播单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        duration_in_second = 5
        frequency = 300
        start_date = tomorrow
        end_date = tomorrow
        ad_unit_type = 'GUARANTEED'
        dsp = False
        suit_codes=global_demo.GL_SUIT_CODES[0]
        ad_campaign_id = ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        result = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type,
                                                  dsp, suit_codes, ad_campaign_id, dsp_id, target_type)
        ad_unit_id = result.json()['adUnitId']
        '''审核计划,审核失败'''
        contract_no = 'contract_no'
        contract_type = 'URGENT'
        result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        content = result.json()
        self.assertEqual(result.status_code, 200, msg='审核计划失败，状态码为200')
        self.assertEqual(content['success'], False, msg='审核计划失败，审核成功状态值为false 则用例通过')
        ad_unit.AdUnit.delete_unit(ad_unit_id)

    def del_test_unit_version_audit_campaign_success(self):
        """接口返回值不返回version，暂不测试加计划审核锁，计划下单元版本号version的测试,审核计划时，计划的任何一个字段值发生变化，计划下单元version+1，否则version保持不变"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []

        ''' 创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text
        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

        '''在计划下创建一个候补单元'''
        tomorrow = time_function.GetTime.get_tomorrow()
        duration_in_second = 5
        frequency = 300
        start_date = tomorrow
        end_date = tomorrow
        ad_unit_type = 'CANDIDATE'
        dsp = False
        suit_codes=global_demo.GL_SUIT_CODES[0]
        ad_campaign_id = ad_campaign_id
        dsp_id = '603fe4897926451ca30e4a2fa8c68ee8'
        target_type = 'SUIT'
        result = ad_unit.AdUnit().create_unit(duration_in_second, frequency, start_date, end_date, ad_unit_type,
                                                  dsp, suit_codes, ad_campaign_id, dsp_id, target_type)
        ad_unit_id = result.json()['adUnitId']
        '''确认单元'''
        ad_unit.AdUnit.confirm_unit(ad_unit_id)
        '''获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        version = result['version']

        '''1：审核计划类型为合同,审核成功，检查单元版本号+1'''
        contract_no = 'contract_no'
        contract_type = 'CONTRACT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
        '''再次获取单元的publishVersion'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version + 1, msg='审核计划成功，状态码为200')
        version = new_version

        '''2: 不解锁，再次审核计划，合同信息无任何变化，审核成功，检查单元版本号不变'''
        contract_no = 'contract_no'
        contract_type = 'CONTRACT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
        '''再次获取单元的publishVersion'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号不变'''
        self.assertEqual(new_version, version, msg='审核计划成功，状态码为200')

        '''3: 不解锁，再次审核计划，修改合同号，审核成功，检查单元版本号+1'''
        contract_no = 'contract_no1'
        contract_type = 'CONTRACT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
        '''再次获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version+1, msg='审核计划成功，状态码为200')
        version = new_version

        '''4: 不解锁，再次审核计划，修改合同类型为急播单，审核成功，检查单元版本号+1'''
        contract_no = 'contract_no1'
        contract_type = 'URGENT'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='', industry='', pb_content='', audit_type='')
        '''再次获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version+1, msg='审核计划成功，状态码为200')
        version = new_version

        '''5: 不解锁，再次审核计划，修改brand，审核成功，检查单元版本号+1'''
        contract_no = 'contract_no1'
        contract_type = 'CONTRACT'
        brand = 'test1'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand, industry='', pb_content='', audit_type='')
        '''再次获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version+1, msg='审核计划成功，状态码为200')
        version = new_version

        '''6: 不解锁，再次审核计划，修改industry，审核成功，检查单元版本号+1'''
        contract_no = 'contract_no1'
        contract_type = 'CONTRACT'
        brand = 'brand'
        industry = 'industry'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand, industry, pb_content='', audit_type='')
        '''再次获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version+1, msg='审核计划成功，状态码为200')
        version = new_version

        '''7: 不解锁，再次审核计划，修改pb_content，审核成功，检查单元版本号+1'''
        contract_no = 'contract_no1'
        contract_type = 'CONTRACT'
        brand = 'brand'
        industry = 'industry'
        pb_content = 'pb_content'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand, industry,
                                                pb_content, audit_type='')
        '''再次获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version + 1, msg='审核计划成功，状态码为200')
        version = new_version

        '''8: 不解锁，再次审核计划，修改audit_type，审核成功，检查单元版本号+1'''
        contract_no = 'contract_no1'
        contract_type = 'CONTRACT'
        brand = 'brand'
        industry = 'industry'
        pb_content = 'pb_content'
        audit_type = 'audit_type'
        ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand, industry,
                                                pb_content, audit_type)
        '''再次获取单元的version'''
        result = ad_unit.AdUnit.get_unit_info(ad_unit_id)
        new_version = result['version']
        '''检查版本号+1'''
        self.assertEqual(new_version, version + 1, msg='审核计划成功，状态码为200')

        '''环境恢复：解锁计划、撤销锁位、并删除单元'''
        ad_campaign.AdCampaign().unlock_campaign(ad_campaign_id)
        ad_unit.AdUnit.revert_unit(ad_unit_id)
        del_result = ad_unit.AdUnit.delete_unit(ad_unit_id)
        self.assertEqual(del_result, True, msg='单元删除成功')

    """各参数等价类测试"""
    def test_audit_campaign_no_contractNo_success(self):
        """ 合同号为空，审核失败，目前报错InternalServerError"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text

        '''审核计划'''
        contract_no = ''
        contract_type = 'CONTRACT'
        result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        content = result.json()
        self.assertEqual(result.status_code, 400, msg='审核计划失败，状态码为500则用例通过')
        self.assertNotEqual(content['code'], 'InternalServerError', msg='审核计划失败，则用例通过')

        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

    def test_audit_campaign_no_contractType_success(self):
        """ 审核类型为空，审核失败，目前报错InternalServerError"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text

        '''审核计划'''
        contract_no = '12344'
        contract_type = ''
        result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        content = result.json()
        self.assertEqual(result.status_code, 400, msg='审核计划失败，状态码为500则用例通过')
        self.assertNotEqual(content['code'], 'InternalServerError', msg='审核计划失败，则用例通过')

        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)

    def test_audit_campaign_noENUM_contractType_success(self):
        """ 审核类型不在ENUM(CONTRACT_URGENT)内，审核失败，目前报错InternalServerError"""
        global_demo.GL_DEL_CAMPAIGN_LIST = []
        '''创建一个计划'''
        refer_id=global_demo.GL_REFER_ID1
        campaign_type = 'KA'
        campaign_name = int(round(time.time() * 1000000))
        result = ad_campaign.AdCampaign.create_campaign(refer_id, campaign_name, campaign_type, note='')
        ad_campaign_id = result.text

        '''审核计划'''
        contract_no = '12344'
        contract_type = 'o'
        result = ad_campaign.AdCampaign().audit_campaign(ad_campaign_id, contract_no, contract_type, brand='',
                                                         industry='', pb_content='', audit_type='')
        content = result.json()
        self.assertEqual(result.status_code, 400, msg='审核计划失败，状态码为500则用例通过')
        self.assertNotEqual(content['code'], 'InternalServerError', msg='审核计划失败，则用例通过')

        global_demo.GL_DEL_CAMPAIGN_LIST.append(ad_campaign_id)
        time.sleep(1)


if __name__ == '__main__':
    pytest.main(["test_campaign_audit.py::TestAuditCampaign::test_audit_pending_campaign_fail"])



