__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'KMLCreator.py'
__version__ = '06.10.2017'

import sqlite3
import simplekml
import gc
import progressbar
from DataCollector import DataCollector

class KMLCreator(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    def createKMLFile_old(self, file):
        dataCollector = DataCollector()
        sqlConnection = sqlite3.connect(file)
        cursor = sqlConnection.cursor()
        coordinates = dataCollector.collect_data_old(cursor)
        size = len(coordinates)

        kml = simplekml.Kml()

        bar = progressbar.ProgressBar()
        for i in bar(range(0, size - 2)):
            lin = kml.newlinestring(name='temp',
                                    coords=[(coordinates[i].getLongitude(),
                                             coordinates[i].getLatitude(),
                                             coordinates[i + 1].getLongitude(),
                                             coordinates[i + 1].getLatitude())])
            lin.style.linestyle.color = simplekml.Color.red

        kmlString = file[0:len(file) - 3] + "_alt.kml"
        kml.save(kmlString)

        # Starting the Python garbage collector
        gc.collect()

        cursor.close()
        sqlConnection.close()

    def createKMLFile_new(self, file):
        dataCollector = DataCollector()
        sqlConnection = sqlite3.connect(file)
        cursor = sqlConnection.cursor()
        coordinates = dataCollector.collect_data_new(cursor)
        size = len(coordinates)

        kml = simplekml.Kml()
        bar = progressbar.ProgressBar()
        for i in bar(range(0, size - 2)):
            lin = kml.newlinestring(name='temp',
                                    coords=[(coordinates[i].getLongitude(),
                                             coordinates[i].getLatitude(),
                                             coordinates[i + 1].getLongitude(),
                                             coordinates[i + 1].getLatitude())])
            lin.style.linestyle.color = simplekml.Color.blue

        KMLString = file[0:len(file) - 3] + "_neu.kml"
        kml.save(KMLString)

        # Starting the Python garbage collector
        gc.collect()

        cursor.close()
        sqlConnection.close()