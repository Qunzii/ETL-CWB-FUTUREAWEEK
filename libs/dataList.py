def fetchDataId(seq, datasetType):
    # Administrative District
    districtDataId_list = ['F-D0047-003', # 宜蘭縣
                             'F-D0047-007', # 桃園市
                             'F-D0047-011', # 新竹縣
                             'F-D0047-015', # 苗栗縣
                             'F-D0047-019', # 彰化縣
                             'F-D0047-023', # 南投縣
                             'F-D0047-027', # 雲林縣
                             'F-D0047-031', # 嘉義縣
                             'F-D0047-035', # 屏東縣
                             'F-D0047-039', # 臺東縣
                             'F-D0047-043', # 花蓮縣
                             'F-D0047-047', # 澎湖縣
                             'F-D0047-051', # 基隆市
                             'F-D0047-055', # 新竹市
                             'F-D0047-059', # 嘉義市
                             'F-D0047-063', # 臺北市
                             'F-D0047-067', # 高雄市
                             'F-D0047-071', # 新北市
                             'F-D0047-075', # 臺中市
                             'F-D0047-079', # 臺南市
                             'F-D0047-083', # 連江縣
                             'F-D0047-087', # 金門縣
                             'F-D0047-091'] # 台灣

    # Attractions
    attractionsDataId_list = ['F-B0053-003', # 海水浴場
                                'F-B0053-009', # 單車
                                'F-B0053-015', # 農場旅遊
                                'F-B0053-021', # 海釣
                                'F-B0053-027', # 娛樂漁業
                                'F-B0053-033', # 登山
                                'F-B0053-039', # 國家公園
                                'F-B0053-045', # 國家風景區
                                'F-B0053-051', # 港口
                                'F-B0053-057', # 國家森林遊樂區
                                'F-B0053-063', # 水庫
                                'F-B0053-069'] # 觀星

    if datasetType == 1:
        if seq < len(districtDataId_list):
            return districtDataId_list[seq]
        else:
            return ''
    elif datasetType == 2:
        if seq < len(attractionsDataId_list):
            return attractionsDataId_list[seq]
        else:
            return ''
