#Program Purpose
#This program will allow the user to evaluate forest are activity in the region chosen. You Will upload a CSV le, the program will output cluster information to about hotspots and are behavior by classifying the different cluster type i.e clumped, dispersed, random. 
import csv
import arcpy

print("Data Input from Modis Forest Fire Occurences")
print()
print("Please input your boundary Shapefile for area of analysis")
print()
input("")

def main():
    File = open (r"blah.csv", "r")
    datafile = csv.reader(File)

    newfile = open (r"exported_data.csv", "w")
    writer = csv.writer(newfile)

    header = next(datafile)
    writer.writerow(header+["", ""])



#*************************************************************

print("Please state a minimum number of features to include in your clusters:  ")
input()
print()
print("Please enter search distance for a clumped cluster:  ")
input()
print()
print("Please enter distance for a dispersed cluster:  ")
input()
print()
print("Please enter year you would like analyzed:   ")
input()
print()
end = input("Do you want to stop entering values (Y/N)?:  ")
        print()
        if  end.upper() == 'Y' :
            break
#*************************************************************



arcpy.env.overwriteOutput = True

firePointsTable = r"C:\GEOM67\GroupProject\BC_fire_points_2019.csv"

arcpy.management.XYTableToPoint(firePointsTable, r"C:\GEOM67\GroupProject\firePoints.shp", 
"longitude", "latitude","","")      # optional parameters: {z_field}, {coordinate_system})

points = r"C:\GEOM67\GroupProject\firePoints.shp"

arcpy.stats.DensityBasedClustering(points, r"C:\GEOM67\GroupProject\pointClusters.shp", 
"HDBSCAN", 15) 
# addiotnal parameters for DBSCAN and OPTICS: ({search_distance}, cluster_sensitivity)