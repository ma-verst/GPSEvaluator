__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'Main.py'
__version__ = '12.10.2017'

import os
from KMLCreator import KMLCreator

####################################################################################################################
# This class acts as the entry point for the program. It goes through all .db files located in the root directory of the
# project and creates for each database .kml and .if files.
# The .kml files can be opened with Google Earth or Google Maps in order to show the trace.
# The .if file has the format "id time_since_start x_coordinate y_coordinate" and is used for a simulator.
####################################################################################################################
def main():
    counter = 0
    kmlCreator = KMLCreator()
    for file in os.listdir(os.curdir):
            if file.endswith(".db"):
                # Creating the .kml file only using the query.
                print("Creating file: "+file+"_alt.kml")
                kmlCreator.createKMLFile_old(file)
                counter += 1

                # Creating the .kml file using the query and considering the velocity.
                print("Creating file: "+file+"_neu.kml")
                kmlCreator.createKMLFile_new(file)
                counter += 1

                # Creating the .if file with Staumuehle as origin of coordinates.
                print("Creating file: "+file+".if")
                kmlCreator.createIFFileFromStaumuehle(file)
                counter += 1
    print "Conversion SUCCESSFUL!"
    print "Created "+str(counter)+" files."

####################################################################################################################
# Starting the program
####################################################################################################################
main()