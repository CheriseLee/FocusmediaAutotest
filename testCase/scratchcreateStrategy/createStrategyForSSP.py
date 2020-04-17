import xlrd
import xlwt
import time_function
import requests
import global_demo
import random
import time
from datetime import datetime,timedelta
"""
为了满足排片上刊的性能测试，对单元进行多样化排播，尽量产生多的排片版本
@lihuanhuan@focusmedia.cn
"""


class CreateStrategy:
    @staticmethod
    def creative_Info_15():
        """配置15s排播的创意信息"""
        creative_info_15 = {
            "186073": "186073_C100828",
            "191738": "191738_C100620",
        }
        return creative_info_15

    @staticmethod
    def creative_Info_30():
        """配置30s排播的创意信息"""
        creative_info_30 = {
            "186073": "186073_C103805",
            "191738": "191738_C103806",
        }
        return creative_info_30

    @staticmethod
    def read_excel(file):
        """打开文件,读取单元的排播信息"""
        wb = xlrd.open_workbook(filename=file)
        sheet1 = wb.sheet_by_index(0)
        total_rows = sheet1.nrows
        unit_list = []
        for i in range(total_rows):
            '''获取行内容'''
            rows = sheet1.row_values(i)
            unit_list.append(rows)
        return unit_list

    @staticmethod
    def set_style(name, height, bold=False):
        '''设置表格样式'''
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    @staticmethod
    def create_unit_strategy(unit,start_date, end_date,product_name):
        ad_unit_id = unit['adUnitId']
        duration = unit['durationInSecond']
        account_id = unit['accountId']
        refer_id = unit['referId']
        creative_group_id_list = CreateStrategy.get_creative_id(duration, account_id,refer_id,product_name)
        while start_date <= end_date:
            for i in range(24):
                creative_group_id = random.choice(creative_group_id_list)
                if i <10 :
                    start_time = '0'+str(i)+':00:00'
                    end_time = '0'+str(i)+':59:59'
                else:
                    start_time = str(i)+':00:00'
                    end_time = str(i)+':59:59'
                payload = {
                    "adUnitId": str(ad_unit_id),
                    "creativeGroupIds": creative_group_id,
                    "startDate": start_date,
                    "startTime": start_time,
                    "endDate": start_date,
                    "endTime": end_time
                }

                url = global_demo.GL_URL_AD_STRATEGY+'/v1/createAdUnitStrategy'
                requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)

            #生成下一天的日期
            date_list = time.strptime(start_date, "%Y-%m-%d")
            y, m, d = date_list[:3]
            delta = timedelta(1)
            date_result = datetime(y, m, d) + delta
            start_date = date_result.strftime("%Y-%m-%d")

    @staticmethod
    def get_units_info(city_id, start_date, end_date,product_name):
        '''查找发布期内涉及发布的单元'''
        payload = {
            "adUnitStatusList": ["WAIT", "SHOW"],
            "cityIdList": [str(city_id)],
            "startDate": start_date,
            "endDate": end_date,
            "productName": product_name,
            "pageNo": 1,
            "pageSize": 10000,
        }
        print(payload)
        get_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/list'
        result = requests.post(get_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()['result']
        return response

    @staticmethod
    def get_creative_id(duration, account_id,refer_id,product_name):
        '''根据账号和单元时长查询匹配到的已审核创意'''
        payload = {
            "accountIds": [account_id],
            "groupDurations": [duration],
            "groupFilters": [
                {
                    "keyword": "STATUS",
                    "values": [
                        "AUDIT_PASS"
                    ]
                }
            ],
            "productName": product_name
        }
        get_creative_url = global_demo.GL_URL_AD_CREATIVE + '/v1/creative-group/list'
        result = requests.post(get_creative_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json().get('data')  #获取创意列表

        # print(type(response))
        creative_id_list=[]
        for key,value in enumerate(response):
            creative_id_list.append(value.get('creativeGroupId'))
        #
        # print(creative_id_list)
        '''创建创意'''
        # nowtime = time.strftime("%Y-%m-%d %H_%M_%S")
        # payload = {
        #     "accountId": account_id,
        #     "adSlot": "FULL_SLOT",
        #     "brandCodes": [
        #         "string"
        #     ],
        #     "creativeGroupName": nowtime,
        #     "creativeGroupSource": "USER_APP",
        #     "groupDurationInSecond": 15,
        #     "creatorId": "string",
        #     "productName": product_name,
        #     "referId": refer_id
        # }
        # create_creative_url = global_demo.GL_URL_AD_CREATIVE + '/v1/creative-group/createAndSave'
        # result = requests.post(create_creative_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # response = result.json().get('creativeGroupId')  #获取创意ID
        #
        # '''审核创意'''


        return creative_id_list




if __name__ == '__main__':
    '''配置城市'''
    city_id = '310000000000'
    product_name= 'SMART_SCREEN'
    '''定义排播的日期'''
    #获取当前发布期排播的起止日期
    # start_date = time_function.GetTime.get_today()
    # end_date = time_function.GetTime.get_this_sunday()

    #获取下一个发布期排播的起止日期
    start_date = time_function.GetTime.get_next_monday()
    end_date = time_function.GetTime.get_next_sunday()

    '''获取需要排播的单元信息'''
    # unit_info = CreateStrategy.get_units_info(city_id, start_date, end_date,product_name)
    #
    # for index,value in enumerate(unit_info):
    #     CreateStrategy.create_unit_strategy(value,start_date, end_date,product_name)





    '''获取排播未排满的单元ID'''
    #先获取全部单元列表
    ad_unit_list = []
    unit_info = CreateStrategy.get_units_info(city_id, start_date, end_date,product_name)
    for key in unit_info:
        ad_unit_list.append(key.get('adUnitId'))
    print('发布期内全部单元数：'+str(len(ad_unit_list)))
    #检查哪些单元排播已完成
    payload = {
               "adUnitIds": ad_unit_list,
       "endDate": end_date,
       "startDate": start_date
    }
    get_unit_url = global_demo.GL_URL_AD_STRATEGY + '/v1/getFullAdUnitIds'
    result = requests.post(get_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
    full_strategy_list =  result.json()
    no_strategy_list = list(set(ad_unit_list)-set(full_strategy_list))

    print('没有排播的单元数：'+str(len(no_strategy_list)))



    for key in no_strategy_list:
        '''获取单元详情'''
        get_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/get/'+ str(key)
        result = requests.get(get_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        unit = result.json()
        ad_unit_id = unit['adUnitId']
        duration = unit['durationInSecond']
        account_id = unit['accountId']
        refer_id = unit['referId']
        creative_group_id_list = CreateStrategy.get_creative_id(duration, account_id,refer_id,product_name)
        '''检查时间呀'''
        start_date = time_function.GetTime.get_next_monday()
        end_date = time_function.GetTime.get_next_sunday()
        while start_date <= end_date:
            for i in range(24):
                creative_group_id = random.choice(creative_group_id_list)
                if i <10 :
                    start_time = '0'+str(i)+':00:00'
                    end_time = '0'+str(i)+':59:59'
                else:
                    start_time = str(i)+':00:00'
                    end_time = str(i)+':59:59'
                payload = {
                    "adUnitId": str(ad_unit_id),
                    "creativeGroupIds": creative_group_id,
                    "startDate": start_date,
                    "startTime": start_time,
                    "endDate": start_date,
                    "endTime": end_time
                }

                url = global_demo.GL_URL_AD_STRATEGY+'/v1/createAdUnitStrategy'
                requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
                time.sleep(1)

            #生成下一天的日期
            date_list = time.strptime(start_date, "%Y-%m-%d")
            y, m, d = date_list[:3]
            delta = timedelta(1)
            date_result = datetime(y, m, d) + delta
            start_date = date_result.strftime("%Y-%m-%d")

