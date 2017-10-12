__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'KMLCreator.py'
__version__ = '12.10.2017'

import sqlite3
from simplekml import Kml, Style
import gc
import progressbar
import math
from DataCollector import DataCollector

####################################################################################################################
# This class provides functions for creating .kml and .if files. The class uses an instance of the DataCollector class
# in order to collect the data in the first step and finally storing the data in either .kml or .if format.
####################################################################################################################
class KMLCreator(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    ####################################################################################################################
    # Creates a .kml file by selecting all coordinates from a database file.
    ####################################################################################################################
    def createKMLFile_old(self, file):
        # Collecting data here
        dataCollector = DataCollector()
        coordinates = dataCollector.collect_data_old(file)

        # Creating kml object and setting the style for the linestring
        kml = Kml()
        sharedstyle=Style()
        sharedstyle.linestyle.color = 'ff0000ff'

        bar = progressbar.ProgressBar()
        # Adding linestrings from the coordinates
        for i in bar(range(0, len(coordinates) - 2)):
            lin = kml.newlinestring(name='{}'.format(coordinates[i].getTimestamp()),
                                    coords=[(coordinates[i].getLongitude(),
                                             coordinates[i].getLatitude()),
                                            (coordinates[i + 1].getLongitude(),
                                             coordinates[i + 1].getLatitude())],)
            lin.style = sharedstyle

        # Setting file name and storing the data in the .kml file
        kmlString = file[0:len(file) - 3] + "_alt.kml"
        kml.save(kmlString)

        # Starting the Python garbage collector
        gc.collect()

    ####################################################################################################################
    # Creates a .kml file by selecting all coordinates from a database file INCLUDING the velocity of the person
    # between two coordinates. If the velocity is higher than a person can run, the coordinates are dropped.
    ####################################################################################################################
    def createKMLFile_new(self, file):
        # Collecting data here
        dataCollector = DataCollector()
        coordinates = dataCollector.collect_data_new(file)

        # Creating kml object and setting the style for the linestring
        kml = Kml()
        sharedstyle = Style()
        sharedstyle.linestyle.color = 'ffff0000'

        bar = progressbar.ProgressBar()
        # Adding linestrings from the coordinates
        for i in bar(range(0, len(coordinates) - 2)):
            lin = kml.newlinestring(name='{}'.format(coordinates[i].getTimestamp()),
                                    coords=[(coordinates[i].getLongitude(),
                                             coordinates[i].getLatitude()),
                                            (coordinates[i + 1].getLongitude(),
                                             coordinates[i + 1].getLatitude())])
            lin.style = sharedstyle
        KMLString = file[0:len(file) - 3] + "_new.kml"
        kml.save(KMLString)

        # Starting the Python garbage collector
        gc.collect()

    ####################################################################################################################
    # Collects data from a database file and converts them into the specified .if format
    # "id time_since_start x_coordinate y_coordinate"
    ####################################################################################################################
    def createIFFileFromStaumuehle(self, file):
        # Collecting data here
        dataCollector = DataCollector()
        coordinates = dataCollector.collect_data_old(file)

        fileString = file[0:len(file) - 3] + ".if"

        f = open('{}'.format(fileString), 'w')
        # Calculating id, time_since_start, x-coordinate, y-coordinate and print them in the file
        for i in range(0, len(coordinates) - 2):
            x, y = self.getDistanceFromStaumuehle(coordinates[i].getLongitude(), coordinates[i].getLatitude())
            timestep = dataCollector.getTimeDifference(coordinates[i].getTimestamp(), '2017-09-02 10:00:00')
            index = i+1
            f.write('{} {} {} {}\n'.format(index, timestep, x, y))
        f.close()

    ####################################################################################################################
    # Calculates the distance, which a person has to walk in x- and y-direction to reach a certain point from the      #
    # starting point in Staumuehle [51.819041,8.727565]                                                                #
    #------------------------------------------------------------------------------------------------------------------#
    # Movement in y-direction responds to traversing latitudes. Here we can take the fix value of 111000 meters per    #
    # latitude. Simply use rule of three to calculate the distance                                                     #
    #------------------------------------------------------------------------------------------------------------------#
    # Movement in x-direction responds to traversing longitudes. Here the difference between two longitudes depends on #
    # latitude. For short distances we can neglect certain factors and approximate a right triangle between the two    #
    # points. In the triangle the hypotenuse is simply the orthodrome (luftlinie) between two points on earth surface. #
    # The y-distance can be simply calculated as stated above. With knowing two sides from a right triangle, the x     #
    # side can be calculated using Pythagoras theorem.                                                                 #
    ####################################################################################################################
    def getDistanceFromStaumuehle(self, longitude, latitude):
        referenceLatitude = 51.819041
        referenceLongitude = 8.727565
        distanceBetweenOneLatitude = 111000

        dataCollector = DataCollector()
        y = (longitude - referenceLongitude)*distanceBetweenOneLatitude
        z = dataCollector.getDistance(latitude,longitude,referenceLatitude,referenceLongitude)
        x = math.sqrt(abs(z*z - y*y))

        # Adaption to coordinate system
        if(x<referenceLongitude):
            x *= -1
        if(y<referenceLatitude):
            y *= -1
        return x,y