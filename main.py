# basic package
import os
import sys
import pytz
import datetime
import requests
import dateutil.parser
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

# custom package
from libs import dataList
from libs import fetchAPIUrl
from libs import getAttributeList
from libs import postgres

# 初始化各連線物件
host = '192.168.63.160'
dbname = 'api'
user = 'postgres'
password = 'postgres'

# 資料類型
datasetType_list = [1,2] # 1 : 行政區；2 : 景點

def parseAPI(connObj, datasetType):
    # 初始化XML資料陣列
    xml_list = []
    
    # 初始化資料集編號陣列
    dataId_list = []
    
    # 初始化資料集計數器
    dataSeq_count = 0
    for dataId_seq in range(23):
        dataId = dataList.fetchDataId(dataId_seq, datasetType)
        if dataId:
            dataUrl = fetchAPIUrl.parse(dataId).getDataUrl()
        else:
            break
        
        xml = requests.get(dataUrl).text.encode('utf-8-sig')
        weather_report = BeautifulSoup(xml, "html.parser")

        xml_list.append(weather_report)
        dataId_list.append(dataId)

    for data_seq in xml_list:
        starttime_list = []
        endtime_list = []
        locations_list = []
        location_list = []
        geocode_list = []
        loccode_list = []
        lati_list = []
        longi_list = []
        result_collection = []

        issuetime = data_seq.find("datasetinfo").find("issuetime")
        county = data_seq.find("locations").find("locationsname")
        starttime = data_seq.find("weatherelement").find_all("starttime")
        endtime = data_seq.find("weatherelement").find_all("endtime")
        city = data_seq.find("locations").find_all("locationname")
        geocode = data_seq.find("locations").find_all("geocode")
        loccode = data_seq.find("locations").find_all("parametervalue")
        lati = data_seq.find("locations").find_all("lat")
        longi = data_seq.find("locations").find_all("lon")

        # 取得現在資料中所有起始時間並加入list
        for starttime_element in starttime:
            starttime_list.append(starttime_element.text)

        # 取得現在資料中所有結束時間並加入list
        for endtime_element in endtime:
            endtime_list.append(endtime_element.text)

        # 取得現在資料中所有的鄉鎮並加入list
        for location_element in city:
            location_list.append(location_element.text)

        # 取得現在資料中所有的區域代碼並加入list
        for geocode_element in geocode:
            geocode_list.append(geocode_element.text)

        # 取得現在資料中所有景點代碼並加入list
        for loccode_element in loccode:
            loccode_list.append(loccode_element.text)

        # 取得現在資料中所有鄉鎮的經度並加入list
        for lati_element in lati:
            lati_list.append(lati_element.text)

        # 取得現在資料中所有鄉鎮的緯度並加入list
        for longi_element in longi:
            longi_list.append(longi_element.text)

        # delete data which already exist
        delVariable = '\'%s\'' * len(starttime_list)
        delVariable = '(' + delVariable.replace('\'\'', '\',\'') + ')'
        delVariable = delVariable.replace('\'', '')
        delData = '''delete from cwb.main_opendata_cwb_futureaweek
                        where start_time in ''' + delVariable + ''' and opendata_id = %s;'''
        deltime_list = starttime_list.copy()
        for deltime_seq in range(len(deltime_list)):
            deltime_list[deltime_seq] = datetime.strftime(dateutil.parser.parse(deltime_list[deltime_seq]).astimezone(pytz.timezone('Asia/Taipei')), "%Y-%m-%d %H:%M:%S")
        deltime_list.append(dataId_list[dataSeq_count])
        delVar = deltime_list

        # get feedback result
        delete = postgres.connection('', '', '', '', connObj, delData, delVar).delete()
        print(delete)

        for data_num in range(len(location_list)):
            for time_num in range(len(starttime_list)):
                result_list = []
                result_list.append(dataId_list[dataSeq_count])
                result_list.append(datetime.strftime(dateutil.parser.parse(issuetime.text).astimezone(pytz.timezone('Asia/Taipei')), "%Y-%m-%d %H:%M:%S"))
                result_list.append(datasetType)
                # geocode : 1 / loccode : 2
                if datasetType == 1:
                    result_list.append(geocode_list[data_num])
                elif datasetType == 2:
                    result_list.append(loccode_list[data_num])
                # locations_list / location_list
                if len(locations_list) == 1 and locations_list[0] == '台灣':
                    result_list.append(location_list[data_num])
                elif datasetType == 2:
                    result_list.append(location_list[data_num])
                else:
                    result_list.append(county.text)
                result_list.append(location_list[data_num])
                result_list.append(lati_list[data_num])
                result_list.append(longi_list[data_num])
                result_list.append(datetime.strftime(dateutil.parser.parse(starttime_list[time_num]).astimezone(pytz.timezone('Asia/Taipei')), "%Y-%m-%d %H:%M:%S"))
                result_list.append(datetime.strftime(dateutil.parser.parse(endtime_list[time_num]).astimezone(pytz.timezone('Asia/Taipei')), "%Y-%m-%d %H:%M:%S"))
                result_list.extend(getAttributeList.get_weather_data(data_seq, location_list[data_num], endtime_list[time_num]))
                result_list.append(datetime.now(pytz.timezone('Asia/Taipei')))

                result_collection.extend(result_list)

        # insert new data
        insVariable = '\'%s\'' * len(result_list)
        insVariable = '(' + insVariable.replace('\'\'', '\',\'') + ')'
        insVariable = insVariable.replace('\'', '')
        insCollection = insVariable * int(len(result_collection) / 29)
        insCollection = insCollection.replace(')(', '), (')
        insData = '''INSERT INTO cwb.main_opendata_cwb_futureaweek
                        (opendata_id, issued_time, location_type, location_id, county, city, latitude, longitude, start_time, end_time, t, td, 
                        rh, maxt, mint, maxat, minat, maxci, minci, pop12h, wd, ws_value, ws_level, 
                        wx_value, wx_unit, uvi_value, uvi_level, weather_desc, lastupddate)
                        VALUES''' + insCollection + ''';'''
        insVar = result_collection
        
        # get feedback result
        insert = postgres.connection('', '', '', '', connObj, insData, insVar).insert()
        print(insert)

        dataSeq_count += 1

# 取得連線物件
connObj = postgres.connection(host, dbname, user, password, '', '', '').getConnectionObject()

# main process
for type_seq in range(len(datasetType_list)):
    parseAPI(connObj, datasetType_list[type_seq])

# 釋放連線物件
postgres.connection('', '', '', '', connObj, '', '').release()