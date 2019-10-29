import global_demo
import unittest
import os
import ad_campaign
import operator
"""
按照创建时间，查询最近的10个计划（工作台左侧）
@lihuanhuan@focusmedia.cn
"""


class AuditCampaign(unittest.TestCase):
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
            global_demo.connection.commit()
        except Exception as e:
            global_demo.connection.rollback()

        '''通过接口查询最近的10个计划ID'''
        result = ad_campaign.AdCampaign.list_campaign()
        '''比较两个列表是否相等'''
        is_equal = operator.eq(search_campaign_list, result)

        self.assertEqual(is_equal, True, msg='对比相等，则用例通过')


if __name__ == '__main__':
    # 构造测试集
    # discover = unittest.TestSuite()
    # discover.addTest(createCampaign("test_createKaVacantCampaign_success"))
    # print(discover)

    #按方法名构造用例集
    # 定义测试用例集

    test_dir = os.path.abspath('.')
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")

    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(discover)


