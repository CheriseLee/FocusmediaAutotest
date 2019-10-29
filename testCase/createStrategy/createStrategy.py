import xlrd
import xlwt
import time_function
import requests
import global_demo
"""
对单元进行排播；
目前仅支持时长为15s、30s的单元；
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
    def create_strategy(unit):
        ad_unit_id = unit['adUnitId']
        start_date = unit['startDate']
        end_date = unit['endDate']
        duration = unit['durationInSecond']
        report_id = unit['referId']
        creative_group_id = CreateStrategy.get_creative_id(duration, report_id)
        payload = {
            "adUnitId": str(ad_unit_id),
            "creativeGroupIds": creative_group_id,
            "startDate": start_date,
            "startTime": "00:00:00",
            "endDate": end_date,
            "endTime": "23:59:59"
        }

        url = 'http://ad-strategy-internal-preonline.fmtest.tech/v1/createAdUnitStrategy'
        requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)

    @staticmethod
    def get_units_info(city_id, start_date, end_date):
        '''查找发布期内涉及发布的单元'''
        payload = {
            "cityId": city_id,
            "startDate": start_date,
            "endDate": end_date
        }
        get_unit_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/listByDateRange'
        result = requests.post(get_unit_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()
        return response

    @staticmethod
    def get_creative_id(duration, report_id):
        if duration == 15:
            creative_id = CreateStrategy.creative_Info_15()[report_id]
            return creative_id
        elif duration == 30:
            creative_id = CreateStrategy.creative_Info_30()[report_id]
            return creative_id


if __name__ == '__main__':
    '''配置城市'''
    city_id = '110000000000'
    '''定义排播的日期'''
    tomorrow = time_function.GetTime.get_tomorrow()
    next_next_sunday = time_function.GetTime.get_next_next_sunday()
    start_date = tomorrow
    end_date = next_next_sunday

    '''获取需要排播的单元信息'''
    unit_info = CreateStrategy.get_units_info(city_id, start_date, end_date)

    for unit in unit_info:
        CreateStrategy.create_strategy(unit)
