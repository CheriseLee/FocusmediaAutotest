import xlrd
import xlwt
import global_demo
import requests
import time
"""

@lihuanhuan@focusmedia.cn
"""


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

def get_all_city_1_location():
    file = 'city1by1.xlsx'
    unit_info = read_excel(file)
    location_info_list = []
    for index, value in (enumerate(unit_info[1:])):
        city_info = {}
        targetId_list = []
        city_info['cityId'] = value[0]
        targetids = value[1]
        targetId_list.append(targetids)
        # city_info['targetIds']=targetIds.append(value[1])
        city_info['targetIds'] = targetId_list
        city_info['goalLocationNum'] = 1
        location_info_list.append(city_info)
    print(location_info_list)

def get_all_city_all_location():

    '''获取全部城市的cityID'''
    payload = {
        "pageNo": 1,
        "pageSize": 10000,
        "scope": "onsale",
        "areaType": "CITY",
        "productName": "SMART_SCREEN"
        }

    url = global_demo.GL_URL_AD_RESOURCE + '/v1/area/queryAreas'
    result = requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
    city_info = result.json().get('result')
    city_id_list=[]
    for key,value in enumerate(city_info):
        city_id_list.append(value.get('areaCode'))

    location_info_list = []
    for city_id in city_id_list:
        '''获取某个城市的全部点位信息'''
        payload = {
            "cityId": str(city_id),
            "productName": "SMART_SCREEN",
            "showFields": {
                "locationId": "undefined"
            }
        }

        url = global_demo.GL_URL_AD_RESOURCE + '/v1/location/queryLocation'
        result = requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        location_info = result.json().get('result')

        city_info = {}
        targetId_list = []
        city_info['cityId'] = city_id
        '''获取点位信息'''
        for index, value in (enumerate(location_info)):

            targetid = value.get('locationId')
            targetId_list.append(str(targetid))
            # city_info['targetIds']=targetIds.append(value[1])
        city_info['targetIds'] = targetId_list
        city_info['goalLocationNum'] = 1
        location_info_list.append(city_info)

        '''单个城市的请求，用完删'''
        # payload['startDate']="2020-05-27"
        # payload['endDate']="2020-05-27"
        # payload['durationInSecond']=15
        # payload['frequency']=300
        # payload['dsp']=False
        # payload['orderItems']=city_info
        # url = 'http://openapi.internal.fmtest.tech/v1/adgroup/createOrder'
        # result=requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
        # response = result.json()
        # print(response)

    '''全部城市的请求'''
    payload['startDate']="2020-05-27"
    payload['endDate']="2020-05-27"
    payload['durationInSecond']=15
    payload['frequency']=300
    payload['dsp']=False
    payload['orderItems']=location_info_list
    url = 'http://openapi.internal.fmtest.tech/v1/adgroup/createOrder'
    result=requests.post(url, json=payload, headers=global_demo.GL_HEADERS, verify=False)
    response = result.json()
    print(response)

    #
    #
    # filename = 'total_city_location.txt'
    # with open(filename, 'w') as file_object:
    #     file_object.write(str(location_info_list))

if __name__ == '__main__':
    # get_all_city_1_location()
    starttime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(starttime)
    get_all_city_all_location()
    endtime = time.strftime("%Y-%m-%d %H_%M_%S")
    print(endtime)