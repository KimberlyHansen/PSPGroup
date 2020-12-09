import arcpy
import csv


arcpy.management.XYTableToPoint("modis_2019_Canada.csv", "output\canadafirepoints.shp", 
    "longitude", "latitude","","")