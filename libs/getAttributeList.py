def get_weather_data(xml, location_, time_):
    all_result = []
    weather_report = xml
    locations = weather_report.find_all("locationname")
    for location in locations:
    # 第一層迴圈先確定地區
        if location.text == location_:
            order = locations.index(location)
            weather_report_modify = weather_report.find_all("location")[order]
            # 為減少查詢時間, 僅留下欲查詢地區的內容
            elems = weather_report_modify.find_all("time")
            for elem in elems:
            # 第二層迴圈取出所有天氣資料
                # start_datatime = elem.find("starttime").text
                end_datatime = elem.find("endtime").text
                if time_ == end_datatime:
                    results = elem.find_all("value")
                    for result in results:
                        all_result.append(result.text)

    if all_result == []:
        return all_result

    # 晚上沒有紫外線及曝曬指數, 所以帶-1 && 無
    if len(all_result) == 16:
        all_result.insert(15, -1)
        all_result.insert(16, "無")

    # 降雨機率如果為空, 轉成0%
    if all_result[9] == " ":
        all_result[9] = "0"

    # print("all_result:++++++++++", all_result)
    return all_result