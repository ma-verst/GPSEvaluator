__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'Point.py'
__version__ = '12.10.2017'

####################################################################################################################
# This class represents a single coordinate and gives Getter and Setter methods to access the data fields.
# Provides standard getter and setter methods and a print function to print the object on the console.
####################################################################################################################
class Point(object):
    def __init__(self, identifier, longitude, latitude, altitude, accuracy, timestamp):
        self.__identifier = identifier
        self.__longitude = longitude
        self.__latitude = latitude
        self.__altitude = altitude
        self.__accuracy = accuracy
        self.__timestamp = timestamp

    def __del__(self):
        pass

    def getIdentifier(self):
        return self.__identifier

    def getLongitude(self):
        return self.__longitude

    def getLatitude(self):
        return self.__latitude

    def getAltitude(self):
        return self.__altitude

    def getAccuracy(self):
        return self.__accuracy

    def getTimestamp(self):
        return self.__timestamp

    def setIdentifier(self, identifier):
        self.__identifier = identifier

    def setLongitude(self, longitude):
        self.__longitude = longitude

    def setLatitude(self, latitude):
        self.__latitude = latitude

    def setAltitude(self, altitude):
        self.__altitude = altitude

    def setAccuracy(self, accuracy):
        self.__accurcay = accuracy

    def setTimestamp(self, timestamp):
        self.__timestamp = timestamp

    def toString(self):
        print "Identifier["+str(self.__identifier)+\
              "] Longitude["+str(self.__longitude)+\
              "] Latitude["+str(self.__latitude)+\
              "] Altitude["+str(self.__altitude)+\
              "] Accuracy["+str(self.__accurcay)+\
              "] Timestamp["+str(self.__timestamp)+"]"