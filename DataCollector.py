__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'DataCollector.py'
__version__ = '06.10.2017'

from Point import Point
import math

# This class provides functions to collect the coordinates from a database based on given filters.
# The result from a query contains the following entries (x can be replaced with the id of a specific entry):
# result[x][0] = longitudes
# result[x][1] = latitudes
# result[x][2] = altitudes
# result[x][3] = accuracies
# result[x][4] = timestamps
class DataCollector(object):

    def __init__(self):
        pass

    def __del__(self):
        pass

    # Collecting data from the database by simply applying a filter in the SQL Query
    def collect_data_old(self, cursor):
        cursor.execute("SELECT longitude,latitude,altitude,accuracy,timestamp FROM gps_data WHERE accuracy<50")
        result = cursor.fetchall()
        size = len(result)

        coordinates = []

        for i in range(0, size - 1):
            coordinates.append(Point(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4]))
        return coordinates

    # Collecting data from the database by simply applying a filter in the SQL Query plus a filter for velocity and time
    def collect_data_new(self, cursor):
        cursor.execute("SELECT longitude,latitude,altitude,accuracy,timestamp FROM gps_data WHERE accuracy<50")
        result = cursor.fetchall()
        result_size = len(result)

        # Set the first values of the results
        coordinates = []
        coordinates.append(Point(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]))

        for i in range(1, result_size - 1):
            long_prev = result[i-1][0]
            lat_prev = result[i-1][1]
            long_new = result[i][0]
            lat_new = result[i][1]

            timestamp_prev = result[i-1][4]
            timestamp_new = result[i][4]

            distance = self.getDistance(lat_prev, long_prev, lat_new, long_new)  # Calculate distance between two coordinates
            time = self.getTimeDifference(timestamp_new, timestamp_prev)

            velocity = self.getVelocity(distance, time)

            if (velocity <= 5.0 and time <= 1):
                coordinates.append(Point(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4]))

        return coordinates

    # Returns the distance in meter between two koordinates using the Haversine Formula
    def getDistance(self, lat1, lon1, lat2, lon2):
        radius = 6371
        lat = math.radians(lat2 - lat1)
        lon = math.radians(lon2 - lon1)

        a = math.sin(lat / 2) * math.sin(lat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.sin(lon / 2) * math.sin(lon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius * c
        return distance * 1000

    # Calculate the time difference in seconds between two timestamps. Return the number of seconds. First the later timestamp, then the earlier timestamp
    def getTimeDifference(self, timestamp2, timestamp1):
        date1 = str(timestamp1)
        date2 = str(timestamp2)

        hour1 = date1[11] + date1[12]
        min1 = date1[14] + date1[15]
        sec1 = date1[17] + date1[18]

        hour2 = date2[11] + date2[12]
        min2 = date2[14] + date2[15]
        sec2 = date2[17] + date2[18]

        hourDiff = int(hour2) - int(hour1)
        minDiff = int(min2) - int(min1)
        secDiff = int(sec2) - int(sec1)

        return hourDiff * 3600 + minDiff * 60 + secDiff

    # Returns the velocity with a given distance and time from two coordinates
    def getVelocity(self, distance, time):
        if (time <= 0):
            return 0
        else:
            return (distance / time)