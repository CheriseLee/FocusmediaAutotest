import xlrd
import xlwt
import global_demo
import requests
import os
import time
import csv
"""
用来导出某个账号下全部的单元信息
@lihuanhuan@focusmedia.cn
"""


class GetUnit:
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
    def write_unit_excel(ad_unit_id_list):
        """查找所有单元信息，写入Excel"""

        f = xlwt.Workbook()
        sheet1 = f.add_sheet('unitInfo', cell_overwrite_ok=True)
        row0 = ["单元ID","投放城市","起始日期","结束日期","时长","  频次","  单元状态","单元类型","购买方式","套装","所需点位数","创建时间","计划ID","计划名称","计划类型","单元审核状态","合同号"," 备注"]
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        for index, ad_unit_id in(enumerate(ad_unit_id_list)):
            search_unit_url = global_demo.GL_URL_AD_GROUP+'/v1/ad/unit/get/' + str(ad_unit_id)
            result = requests.get(search_unit_url,  headers=global_demo.GL_HEADERS, verify=False)
            value=result.json()


            '''写单元信息'''
            sheet1.write(index+1, 0, value.get("adUnitId"))
            sheet1.write(index+1, 1, value.get("cityId"))
            sheet1.write(index+1, 2, value.get("startDate"))
            sheet1.write(index+1, 3, value.get("endDate"))
            sheet1.write(index+1, 4, value.get("durationInSecond"))
            sheet1.write(index+1, 5, value.get("frequency"))
            sheet1.write(index+1, 6, value.get("adUnitStatus"))
            sheet1.write(index+1, 7, value.get("adUnitType"))
            sheet1.write(index+1, 8, value.get("targetType"))
            sheet1.write(index + 1, 10, value.get("goalLocationNum"))
            sheet1.write(index + 1, 11, value.get("updateTime"))
            sheet1.write(index + 1, 12, value.get("adCampaignId"))
            sheet1.write(index + 1, 13, value.get("adCampaignName"))
            sheet1.write(index + 1, 14, value.get("adCampaignType"))
            sheet1.write(index + 1, 15, value.get("auditStatus"))
            sheet1.write(index + 1, 16, value.get("contractNo"))
            sheet1.write(index + 1, 17, value.get("note"))
            #套装
            if value.get("targetType")=='SUIT':

                suit_list = []
                suitList=value.get("adUnitItemList")
                # print(suitList)
                # print(type(suitList))
                for new_index,value in enumerate(suitList):
                    # print(value)
                    suit_list.append(";"+value.get("targetId"))
                sheet1.write(index + 1, 9,suit_list)
                sheet1.write(index + 1, 18, len(suit_list))

            # sheet1.write(index+1, 16, unit_detail_info.get("fakeSuitInfo"))

            # sheet1.write(1,3,'2006/12/12')
            # sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
            # sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
            # sheet1.write_merge(4,5,3,3,'打篮球')

            f.save('test.csv')

    def get_campaign_list(self,refer_id):
        '''获取每个账号下的全部计划ID'''
        payload = {
            "referIdList": [refer_id],
            "pageNo": 1,
            "pageSize": 10000,
            "productName": "SMART_SCREEN"
        }
        '''创建单元'''
        get_campaign_list_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/campaign/list'
        result = requests.post(get_campaign_list_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()
        info=response['result']
        # print(info)
        # print(type(info))
        ad_campaign_list=[]
        for key in info:
            ad_campaign_id=key['adCampaignId']
            ad_campaign_list.append(ad_campaign_id)

        return ad_campaign_list

    def get_unit_info(self,ad_campaign_list):
        '''根据计划ID查询全部单元，包括意向中、已取消、已终止'''
        payload = {
            "adCampaignIdList": ad_campaign_list,
            "startDate": "2018-01-12",
            "endDate": "2023-08-12",
            "pageNo": 1,
            "pageSize": 1000000,
        }
        '''创建单元'''
        get_unit_list_url = global_demo.GL_URL_AD_GROUP + '/v1/ad/unit/list'
        result = requests.post(get_unit_list_url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        response = result.json()
        info=response['result']
        # print(info)
        # print(type(info))
        # ad_unit_list=[]
        # for key in info:
        #     ad_unit_id=key['adUnitId']
        #     ad_unit_list.append(ad_unit_id)

        return info

    def write_unit_info_excel(self,unitinfo):
        headers = ['adUnitId', 'cityId', 'adUnitType', 'adUnitStatus', 'startDate', 'endDate', 'realEndDate','hours', 'durationInSecond', 'frequency',
                   'targetType', 'targetCount', 'goalLocationNum', 'adUnitItemList', 'referId', 'referName', 'adCampaignId',
                   'adCampaignName', 'adCampaignType', 'auditStatus'
                                                      , 'resourceVersion', 'dspId', 'reserved', 'excludeTargetType',
                   'baseAdUnitId', 'adUnitCount', 'publishVersion', 'dsp', 'publishChanged', 'source', 'creator',
                   'errorTargetIds', 'brand', 'contractType', 'resourceAreaType', 'pbContent', 'accountId', 'published',
                   'updateTime', 'urgentExpireDate', 'note', 'contractNo', 'fakeSuitInfo', 'preemptive', 'createTime',
                   'productName', 'publishTime', 'fakeSuit', 'endTime', 'industry',
                   'auditType', 'excludeTargetIds'
                   ]
        rows = unitinfo
        with open('unitinfo.csv', 'a+', newline='', encoding='utf-8_sig') as f:
            f_scv = csv.DictWriter(f, headers)
            f_scv.writeheader()
            f_scv.writerows(rows)

def replace_str():
    # file1 = open('test.csv', 'r',encoding='utf-8_sig').readlines()
    file1 = open('test.csv', 'r',encoding='gbk').readlines()
    # file1 = open('test.csv', 'r').readlines()
    curtime = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = '单元详情'+curtime +'.csv'
    # print(filename)
    fileout = open(filename, 'w', encoding='utf-8_sig')
    for index, line in enumerate(file1):

        l1 = line.replace('GUARANTEED', '必播')
        l2 = l1.replace('CANDIDATE_NON_PREEMPTIVE', '候补非抢占')
        l3 = l2.replace('CANDIDATE', '候补可抢占')
        l4 = l3.replace('PENDING', '意向中')
        l5 = l4.replace('WAIT', '待发布')
        l6 = l5.replace('SHOW', '发布中')
        l7 = l6.replace('BUILDING', '物业')
        l8 = l7.replace('NONPROFIT', '公益')
        l9 = l8.replace('VACANT', '空位')

    fileout.writelines(file1)
    fileout.close()

    '''删除旧文件'''
    if os.path.exists('operateRecord.csv'):
        os.remove('operateRecord.csv')

if __name__ == '__main__':
    refer_id='136774'
    # refer_id='136626'
    starttime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(starttime)
    '''获取账号的全部计划信息'''
    ad_campaign_id_list = GetUnit().get_campaign_list(refer_id)
    '''获取计划下全部的单元信息'''
    ad_unit_info=GetUnit().get_unit_info(ad_campaign_id_list)
    # print(ad_unit_info)
    GetUnit().write_unit_info_excel(ad_unit_info)
    # replace_str()
    endtime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(endtime)