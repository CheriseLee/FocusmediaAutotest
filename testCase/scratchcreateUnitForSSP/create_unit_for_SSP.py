import xlrd
import xlwt
import global_demo
import requests
import time_function
"""
Excel中报备号务必是：186073_118327、191738_118326
Excel中的数据为北京的，包括城市ID,项目ID,套装编号等信息，故SSP测试务必选择北京这个城市；
执行之前，务必先清空北京原有订单及库存，产生一个干净的环境
@lihuanhuan@focusmedia.cn
"""


class CreateUnit:
    @staticmethod
    def read_excel(file):
        """打开Excel，读取创建单元的信息，每一行为1个单元"""
        wb = xlrd.open_workbook(filename=file)
        '''过索引获取表格'''
        sheet1 = wb.sheet_by_index(0)
        '''获取表格的总行数'''
        total_rows = sheet1.nrows
        unit_list = []
        for i in range(total_rows):
            '''获取行内容'''
            rows = sheet1.row_values(i)
            unit_list.append(rows)
        return unit_list

    @staticmethod
    def set_style(name, height, bold=False):
        """设置表格样式"""
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    @staticmethod
    def write_unit_excel(ad_unit_list):
        """查找所有单元信息，写入Excel"""
        payload = {}

        f = xlwt.Workbook()
        sheet1 = f.add_sheet('unitInfo', cell_overwrite_ok=True)
        row0 = ["单元Id", "单元类型", "单元状态", "城市ID", "起始日期", "终止日期", "小时", "时长", "频次", "是否程序化", "目标类型", "所需点位数", "计划ID", "计划名称",
                "计划类型", "报备号", "模拟套装名称"]

        for index, value in(enumerate(ad_unit_list)):
            search_unit_url = global_demo.GL_URL_AD_GROUP+'/v1/ad/unit/get/' + str(value)
            result = requests.get(search_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
            unit_detail_info=result.json()

            '''写第一行'''
            if index == 0:
                for i in range(0, len(row0)):
                    sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
            '''写单元信息'''
            sheet1.write(index+1, 0, unit_detail_info.get("adUnitId"))
            sheet1.write(index+1, 1, unit_detail_info.get("adUnitType"))
            sheet1.write(index+1, 2, unit_detail_info.get("adUnitStatus"))
            sheet1.write(index+1, 3, unit_detail_info.get("cityId"))
            sheet1.write(index+1, 4, unit_detail_info.get("startDate"))
            sheet1.write(index+1, 5, unit_detail_info.get("endDate"))
            sheet1.write(index+1, 6, unit_detail_info.get("hours"))
            sheet1.write(index+1, 7, unit_detail_info.get("durationInSecond"))
            sheet1.write(index+1, 8, unit_detail_info.get("frequency"))
            sheet1.write(index+1, 9, unit_detail_info.get("dsp"))
            sheet1.write(index+1, 10, unit_detail_info.get("targetType"))
            sheet1.write(index+1, 11, unit_detail_info.get("goalLocationNum"))
            sheet1.write(index+1, 12, unit_detail_info.get("adCampaignId"))
            sheet1.write(index+1, 13, unit_detail_info.get("adCampaignName"))
            sheet1.write(index+1, 14, unit_detail_info.get("adCampaignType"))
            sheet1.write(index+1, 15, unit_detail_info.get("referId"))
            sheet1.write(index+1, 16, unit_detail_info.get("fakeSuitInfo"))

            # sheet1.write(1,3,'2006/12/12')
            # sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
            # sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
            # sheet1.write_merge(4,5,3,3,'打篮球')

            f.save('test.xls')

    @staticmethod
    def create_units(index, value, start_date, end_date):
        """创建单元"""
        adUnitTargetIds = value[10].split(",")
        payload = {
            "adCampaignId": value[0],
            "cityId": str(value[1]),
            "durationInSecond": value[2],
            "frequency": value[3],
            "startDate": start_date,
            "endDate": end_date,
            # "hours": [],
            "adUnitType": value[5],
            "targetType": value[6],
            "dsp": value[7],
            "productName": value[8],
            "submitType": value[9],
            "adUnitTargetIds": adUnitTargetIds,
            "goalLocationNum": value[11],
            "dspId": value[12]
        }
        '''创建单元'''
        create_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/create'
        result = requests.post(create_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()
        if "adUnitId" in response.keys():
            pass
        else:
            print(index + "创建失败")
            print(response)

    @staticmethod
    def reserve_unit():
        """对必播单元进行锁位"""
        '''查找数据库里意向中的必播单元'''
        cursor = global_demo.GL_CONNECTION.cursor()
        sql = "SELECT * FROM ad_unit WHERE city_id='310000000000' AND ad_unit_type='GUARANTEED' AND ad_unit_status='PENDING' "
        cursor.execute(sql)
        '''获取所有记录列表'''
        results = cursor.fetchall()
        for key in results:
            ad_unit_id = key.get("ad_unit_id")
            payload = {
                "adUnitId": ad_unit_id
            }
            reserve_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/reserve'
            result = requests.post(reserve_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
            response = result.json()
            if response.get("success"):
                ad_unit_id_list.append(response.get("adUnitId"))
            else:
                # print(response.get("adUnitId")+"库存不足，锁位失败")
                continue


    @staticmethod
    def confirm_unit():
        """对候补单元进行确认"""
        '''查找所有的意向中候补单'''
        cursor = global_demo.GL_CONNECTION.cursor()
        sql = "SELECT * FROM ad_unit WHERE city_id='310000000000' AND ad_unit_type not in('GUARANTEED') AND ad_unit_status='PENDING' "
        cursor.execute(sql)
        results = cursor.fetchall()
        for key in results:
            payload = {}
            '''确认'''
            confirm_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/confirm/' + str(key.get("ad_unit_id"))
            requests.post(confirm_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        return


    def unlock_campaign(self,city_id,start_date, end_date,product_name):
        '''解锁计划'''
        '''获取城市对应的全部计划'''
        campaign_list = CreateUnit.get_campaign_list(city_id, start_date, end_date, product_name)
        for ad_campaign_id in (campaign_list):
            unlock_campaign = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/unLock/' + ad_campaign_id
            requests.post(unlock_campaign, headers=global_demo.GL_HEADERS, verify=False)

    def audit_campaign(self,city_id,start_date, end_date,product_name):
        '''获取城市对应的全部计划'''
        campaign_list = CreateUnit().get_campaign_list(city_id,start_date, end_date, product_name)
        '''删除城市下全部意向中单元'''
        # CreateUnit().delete_pengding_unit(city_id, product_name)

        for index,value in enumerate(campaign_list):
            '''审核计划'''
            payload = {
                "adCampaignId": value,
                "contractNo": str(index),
                "industry": str(index),
                "brand": str(index),
                "pbContent": str(index),
                "auditType": "合同内",
                "contractType": "CONTRACT"
            }
            confirm_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/auditAndBindContract'
            requests.post(confirm_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)

    def get_campaign_list(self,city_id,start_date, end_date,product_name):
        '''查找发布期内涉及发布的单元'''
        payload = {
            "adUnitStatusList": ["WAIT", "SHOW"],
            "cityId": city_id,
            "startDate": start_date,
            "endDate": end_date,
            "productName": product_name,
            "pageNo": 1,
            "pageSize": 10000,
        }
        get_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/list'
        result = requests.post(get_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()['result']
        campaign_list=[]
        for key in response:
            campaign_list.append(key.get('adCampaignId'))
        return campaign_list

    def delete_pengding_unit(self,city_id, product_name):
        '''查找发布期内所有意向中的单元'''
        payload = {
            "adUnitStatusList": ["PENDGING"],
            "cityId": city_id,
            "productName": product_name,
            "pageNo": 1,
            "pageSize": 10000,
        }
        get_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/list'
        result = requests.post(get_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()['result']
        ad_unit_list = []
        for key in response:
            ad_unit_list.append(key.get('adUnitId'))

        '''删除意向中单元'''
        payload =  ad_unit_list
        del_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/batchDelete'
        requests.post(del_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)


if __name__ == '__main__':
    '''配置创建的订单信息文件'''
    city_id = '310000000000'
    file = 'createUnit%s.xlsx'%city_id
    product_name='SMART_SCREEN'
    # file = 'createUnitTest.xlsx'

    tomorrow = time_function.GetTime.get_tomorrow()
    this_sunday = time_function.GetTime.get_this_sunday()
    next_next_sunday = time_function.GetTime.get_next_next_sunday()

    '''定义单元的发布期'''
    start_date = tomorrow
    # end_date = next_next_sunday
    end_date = this_sunday

    '''从Excel里读取要创建的单元的信息'''
    # unit_info = CreateUnit.read_excel(file)
    # ad_unit_id_list = []
    '''创建单元'''
    # for index, value in (enumerate(unit_info[1:])):
    #     CreateUnit.create_units(index, value, start_date, end_date)
    '''对必播单元进行锁位'''
    # CreateUnit.reserve_unit()
    '''对候补单元进行确认'''
    # CreateUnit.confirm_unit()
    '''审核计划'''
    CreateUnit().audit_campaign(city_id, start_date, end_date, product_name)
    # CreateUnit.audit_campaign(city_id)