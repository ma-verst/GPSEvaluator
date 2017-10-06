__author__ = 'Marcel Verst'
__project__ = 'GPSEvaluator'
__className__ = 'Main.py'
__version__ = '06.10.2017'

import os
from KMLCreator import KMLCreator

def main():
    counter = 0
    kmlCreator = KMLCreator()
    for file in os.listdir(os.curdir):
            if file.endswith(".db"):
                print("Creating file: "+file+"_alt.kml")
                kmlCreator.createKMLFile_old(file)
                counter += 1
                print("Creating file: "+file+"_neu.kml")
                kmlCreator.createKMLFile_new(file)
                counter += 1
    print "Conversion SUCCESSFUL!"
    print "Created "+str(counter)+" files."
main()