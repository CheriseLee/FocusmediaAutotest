import global_demo
import unittest
import os
import ad_campaign
import operator
import pytest
import time
"""
按照创建时间，查询最近的10个计划（工作台左侧）
@lihuanhuan@focusmedia.cn
"""


class TestListCampaign():
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_list_campaign_success(self):
        """查询最近的10个计划（工作台左侧）"""
        '''查找数据库里最近的10个计划ID'''
        cursor = global_demo.GL_CONNECTION.cursor()
        sql = "SELECT ad_campaign_id FROM `kuma_ad_group`.`ad_campaign` ORDER BY create_time DESC LIMIT 10"
        '''执行sql语句，避免sql执行失败产生死锁'''
        try:
            cursor.execute(sql)
            search_result = cursor.fetchall()
            search_campaign_list = []
            for key in search_result:
                search_campaign_list.append(key['ad_campaign_id'])
            global_demo.GL_CONNECTION.commit()
        except Exception as e:
            global_demo.GL_CONNECTION.rollback()

        '''通过接口查询最近的10个计划ID'''
        result = ad_campaign.AdCampaign.list_campaign()
        '''比较两个列表是否相等'''
        search_campaign_list.sort()
        result.sort()
        is_equal = operator.eq(search_campaign_list, result)

        self.assertEqual(is_equal, True, msg='对比相等，则用例通过')


if __name__ == '__main__':
    dir_path = os.path.abspath('.')
    # 存放报告的文件夹
    report_dir = dir_path + '\\testReport\\'
    # 报告命名时间格式化
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # 报告文件完整路径
    report_name = 'KUMA接口自动化测试报告' + now + '.html'
    print(report_name)

    # 指定运行某个目录下的某个用例
    pytest.main(["testCase/campaign/test_campaign_list.py",
                 "--html=testReport/%s" % (report_name)])


