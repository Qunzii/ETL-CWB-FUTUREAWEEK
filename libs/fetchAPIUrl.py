class parse():
    def __init__(self, dataId):
        self.dataId = dataId

    def getDataUrl(self):
        authorizationKey = 'CWB-ADBC3A00-9FA4-472E-90FC-40116A25DCA5'
        url = 'http://opendata.cwb.gov.tw/opendataapi?dataid=' + self.dataId + '&authorizationkey=' + authorizationKey

        return url
