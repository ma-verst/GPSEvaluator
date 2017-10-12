__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'DataCollector.py'
__version__ = '12.10.2017'

from Point import Point
import sqlite3
import math

####################################################################################################################
# This class provides functions to collect the coordinates from a database based on given filters.
# The result from a query contains the following entries (x can be replaced with the id of a specific entry):
# result[x][0] = identifier
# result[x][1] = longitudes
# result[x][2] = latitudes
# result[x][3] = altitudes
# result[x][4] = accuracies
# result[x][5] = timestamps
####################################################################################################################
class DataCollector(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    ####################################################################################################################
    # Collecting all data from the database by a SQL Query.
    ####################################################################################################################
    def collect_data_old(self, file):
        # Connect to file.
        sqlConnection = sqlite3.connect(file)
        cursor = sqlConnection.cursor()

        # Apply query and catch result.
        cursor.execute("SELECT _id,longitude,latitude,altitude,accuracy,timestamp FROM gps_data")
        result = cursor.fetchall()

        # Disconnect from file.
        cursor.close()
        sqlConnection.close()

        # Apppend coordinates.
        coordinates = []
        for i in range(0, len(result) - 1):
            coordinates.append(Point(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5]))
        return coordinates

    ####################################################################################################################
    # Collecting data from the database by simply using a SQL Query plus a filter for velocity and time.
    ####################################################################################################################
    def collect_data_new(self, file):
        # Connect to file.
        sqlConnection = sqlite3.connect(file)
        cursor = sqlConnection.cursor()

        # Apply query and catch result.
        cursor.execute("SELECT _id,longitude,latitude,altitude,accuracy,timestamp FROM gps_data")
        result = cursor.fetchall()

        # Disconnect from file.
        cursor.close()
        sqlConnection.close()

        # Set the first values of the results
        coordinates = []
        coordinates.append(Point(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5]))

        # Append coordinates based on velocity
        for i in range(1, len(result) - 1):
            long_prev = result[i-1][1]
            lat_prev = result[i-1][2]
            long_new = result[i][1]
            lat_new = result[i][2]

            timestamp_prev = result[i-1][5]
            timestamp_new = result[i][5]

            distance = self.getDistance(lat_prev, long_prev, lat_new, long_new)  # Calculate distance between two coordinates
            time = self.getTimeDifference(timestamp_new, timestamp_prev)

            velocity = self.getVelocity(distance, time)

            if (velocity <= 5.0 and time <= 1):
                coordinates.append(Point(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5]))

        return coordinates

    ####################################################################################################################
    # Returns the distance in meter between two coordinates using the Haversine formula
    ####################################################################################################################
    def getDistance(self, lat1, lon1, lat2, lon2):
        radius = 6371
        lat = math.radians(lat2 - lat1)
        lon = math.radians(lon2 - lon1)

        a = math.sin(lat / 2) * math.sin(lat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.sin(lon / 2) * math.sin(lon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius * c
        return distance * 1000

    ####################################################################################################################
    # Returns the time difference in seconds between two timestamps. First argument is the later timestamp, second
    # argument is the earlier timestamp.
    ####################################################################################################################
    def getTimeDifference(self, timestamp_later, timestamp_earlier):
        date_earlier = str(timestamp_earlier)
        date_later = str(timestamp_later)

        hour1 = date_earlier[11] + date_earlier[12]
        min1 = date_earlier[14] + date_earlier[15]
        sec1 = date_earlier[17] + date_earlier[18]

        hour2 = date_later[11] + date_later[12]
        min2 = date_later[14] + date_later[15]
        sec2 = date_later[17] + date_later[18]

        hourDiff = int(hour2) - int(hour1)
        minDiff = int(min2) - int(min1)
        secDiff = int(sec2) - int(sec1)

        return hourDiff * 3600 + minDiff * 60 + secDiff

    ####################################################################################################################
    # Returns the velocity with a given distance and time from two coordinates.
    ####################################################################################################################
    def getVelocity(self, distance, time):
        if (time <= 0):
            return 0
        else:
            return (distance / time)