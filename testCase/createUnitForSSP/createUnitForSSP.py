import xlrd
import xlwt
import global_demo
from urllib import request
import requests
import unittest


# file = 'createUnit110000000000.xlsx'
file = 'createUnitTest.xlsx'


def read_excel():

    wb = xlrd.open_workbook(filename=file)#打开文件
    # print(wb.sheet_names())#获取所有表格名字

    sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    #获取表格的总行数
    totalRows=sheet1.nrows
    totalCols=sheet1.ncols
    unitList = []
    for i in range(totalRows):

        rows = sheet1.row_values(i)#获取行内容
        unitList.append(rows)
    return unitList

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

#写Excel
def write_Unit_excel(ad_unit_id_list):
    payload = {}

    f = xlwt.Workbook()
    sheet1 = f.add_sheet('unitInfo', cell_overwrite_ok=True)
    row0 = ["单元Id", "单元类型", "单元状态", "城市ID", "起始日期", "终止日期", "小时", "时长", "频次", "是否程序化", "目标类型", "所需点位数", "计划ID", "计划名称",
            "计划类型", "报备号", "模拟套装名称"]

    for index,value in(enumerate(ad_unit_id_list)):
        print(index,value)
        searchUnitUrl = global_demo.GL_baseURL_ad_Group+'/v1/ad/unit/get/' + str(value)
        result = requests.get(searchUnitUrl, json=payload, headers=global_demo.GL_headers, verify=False)
        unitDetailInfo=result.json()

        #写第一行
        if index==0:
            for i in range(0,len(row0)):
                sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
        #写单元信息
        sheet1.write(index+1, 0, unitDetailInfo.get("adUnitId"))
        sheet1.write(index+1, 1, unitDetailInfo.get("adUnitType"))
        sheet1.write(index+1, 2, unitDetailInfo.get("adUnitStatus"))
        sheet1.write(index+1, 3, unitDetailInfo.get("cityId"))
        sheet1.write(index+1, 4, unitDetailInfo.get("startDate"))
        sheet1.write(index+1, 5, unitDetailInfo.get("endDate"))
        sheet1.write(index+1, 6, unitDetailInfo.get("hours"))
        sheet1.write(index+1, 7, unitDetailInfo.get("durationInSecond"))
        sheet1.write(index+1, 8, unitDetailInfo.get("frequency"))
        sheet1.write(index+1, 9, unitDetailInfo.get("dsp"))
        sheet1.write(index+1, 10, unitDetailInfo.get("targetType"))
        sheet1.write(index+1, 11, unitDetailInfo.get("goalLocationNum"))
        sheet1.write(index+1, 12, unitDetailInfo.get("adCampaignId"))
        sheet1.write(index+1, 13, unitDetailInfo.get("adCampaignName"))
        sheet1.write(index+1, 14, unitDetailInfo.get("adCampaignType"))
        sheet1.write(index+1, 15, unitDetailInfo.get("referId"))
        sheet1.write(index+1, 16, unitDetailInfo.get("fakeSuitInfo"))

        # sheet1.write(1,3,'2006/12/12')
        # sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
        # sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
        # sheet1.write_merge(4,5,3,3,'打篮球')

        f.save('test.xls')

def createUnits(index,value):
    if(value[8]=='SUIT'):
        suitCodes=value[13].split(",")
        payload = {
            "adCampaignId": value[0],
            "cityId": str(value[1]),
            "durationInSecond": value[2],
            "frequency": value[3],
            "startDate": value[4],
            "endDate": value[5],
            # "hours": [],
            "adUnitType": value[7],
            "targetType": value[8],
            "dsp": value[9],
            "productName": value[10],
            # "buildingIds": [
            #     unitInfo[11]
            # ],
            "submitType":value[12],
            "suitCodes":suitCodes,
            # "goalLocationNum": unitInfo[14],
            "dspId":value[15]
        }
    elif (value[8]=='LOCATION'):
        buildingIds=value[11].split(",")
        payload = {
            "adCampaignId": value[0],
            "cityId": str(value[1]),
            "durationInSecond": value[2],
            "frequency": value[3],
            "startDate": value[4],
            "endDate": value[5],
            # "hours": [],
            "adUnitType": value[7],
            "targetType": value[8],
            "dsp": value[9],
            "productName": value[10],
            "buildingIds": buildingIds,
            "submitType":value[12],
            # "suitCodes":unitInfo[13],
            "goalLocationNum": value[14],
            "dspId":value[15]
        }
    elif (value[8]=='CITY'):
        payload = {
            "adCampaignId": value[0],
            "cityId": str(value[1]),
            "durationInSecond": value[2],
            "frequency": value[3],
            "startDate": value[4],
            "endDate": value[5],
            # "hours": [],
            "adUnitType": value[7],
            "targetType": value[8],
            "dsp": value[9],
            "productName": value[10],
            # "buildingIds": buildingIds,
            "submitType":value[12],
            # "suitCodes":unitInfo[13],
            "goalLocationNum": value[14],
            "dspId":value[15]
        }
#创建单元
    createUnitUrl =global_demo.GL_baseURL_ad_Group + '/v1/ad/unit/create'
    result = requests.post(createUnitUrl, json=payload, headers=global_demo.GL_headers, verify=False)
    response=result.json()
    if("adUnitId" in response.keys()):
        pass
    else:
        print(response)

def reserveUnit():
    # 通过cursor创建游标
    cursor = global_demo.GL_connection.cursor()
    # 创建sql 语句
    sql = "SELECT * FROM ad_unit WHERE city_id='310000000000' AND ad_unit_type='GUARANTEED' AND ad_unit_status='PENDING' "
    # 执行sql语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for key in results:
        ad_unit_id = key.get("ad_unit_id")
        # 锁位
        payload = {
            "adUnitId": ad_unit_id
        }
        reserveuniturl = global_demo.GL_baseURL_ad_Group + '/v1/ad/unit/reserve'
        result = requests.post(reserveuniturl, json=payload, headers=global_demo.GL_headers, verify=False)
        response = result.json()
        if (response.get("success")):
            ad_unit_id_list.append(response.get("adUnitId"))
        else:
            print(response.get("adUnitId")+"库存不足，锁位失败")
            continue

def confirmUnit():
    # 通过cursor创建游标
    cursor = global_demo.GL_connection.cursor()
    # 创建sql 语句
    sql = "SELECT * FROM ad_unit WHERE city_id='310000000000' AND ad_unit_type not in('GUARANTEED') AND ad_unit_status='PENDING' "
    # 执行sql语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for key in results:
        payload = {}
        # 确认
        confirmUnitUrl = global_demo.GL_baseURL_ad_Group + '/v1/ad/unit/confirm/' + str(key.get("ad_unit_id"))
        result = requests.post(confirmUnitUrl, json=payload, headers=global_demo.GL_headers, verify=False)

unitInfo = read_excel()
ad_unit_id_list = []
for index, value in (enumerate(unitInfo[1:])):
    createUnits(index, value)
reserveUnit()
confirmUnit()
# write_Unit_excel(ad_unit_id_list)