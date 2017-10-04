__author__ = 'Marcel Verst'
__project__ = 'GeoEvaluator'
__className__ = 'Evaluator.py'
__version__ = '04.10.2017'

class Evaluator(object):
    __longitude = []
    __latitude = []
    __altitude = []
    pass

    def __init__(self):
        pass

    def __del__(self):
        print "Destruktor gestartet"

    def getData(self, SQLQuery):
        pass
    def filterData(self):
        pass
    def createKML(self):
        pass

    def getLongitude(self):
        return self.__longitude
    def getLatitude(self):
        return self.__latitude
    def getAltitude(self):
        return self.__altitude