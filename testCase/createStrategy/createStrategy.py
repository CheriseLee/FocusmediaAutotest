import xlrd
import xlwt
from urllib import request
import requests
import global_demo

file = 'createStrategy.xls'

def creative_Info():
    creative_Info={
        "186073": "186073_C100828",  #15s
        "191738": "191738_C100620",   #15s
        "start_date":"2019-09-30",
        "end_date":"2019-10-13"
    }
    return creative_Info

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
def write_Strategy_excel():
    try:
        # 通过cursor创建游标
        cursor = global_demo.GL_connection.cursor()
        # 创建sql 语句
        sql = "SELECT * FROM ad_unit WHERE city_id='110000000000' AND ad_unit_status in ('WAIT','SHOW')"
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except  Exception:
        print("查询失败")
    # 关闭游标连接
    cursor.close()
#创建Excel
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('unitStrategyInfo', cell_overwrite_ok=True)
    row0 = ["adUnitId", "creativeGroupIds", "startDate", "startTime", "endDate", "endTime"]
    for i in range(0, len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    for index,value in(enumerate(results)):
        #获取该单元对应的创意组
        ad_campaign_id=value.get("ad_campaign_id")
        listRefer=ad_campaign_id.split("_")
        referid=listRefer[0]
        creative_group_id=creative_Info().get(referid)
        #写单元信息
        sheet1.write(index+1, 0, value.get("ad_unit_id"))
        sheet1.write(index+1, 1, creative_group_id)
        sheet1.write(index+1, 2, creative_Info().get("start_date"))
        sheet1.write(index+1, 3, "00:00:00")
        sheet1.write(index+1, 4, creative_Info().get("end_date"))
        sheet1.write(index+1, 5, "23:59:59")
    f.save('createStrategy.xls')

def createStrategy(unitInfo):
    payload = {
        "adUnitId": str(unitInfo[0]),
        "creativeGroupIds": [unitInfo[1]],
        "startDate": unitInfo[2],
        "startTime": unitInfo[3],
        "endDate": unitInfo[4],
        "endTime": unitInfo[5]
    }

    url = 'http://ad-strategy-internal-preonline.fmtest.tech/v1/createAdUnitStrategy'
    r = requests.post(url, json=payload, headers=global_demo.GL_headers, verify=False)
    # print(r.json())

unitInfo = read_excel()

write_Strategy_excel()
for i in (unitInfo[1:]):
    createStrategy(i)