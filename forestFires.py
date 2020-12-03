# Program Purpose
# This program will allow the user to evaluate forest are activity in the region chosen. 
# You Will upload a CSV le, the program will output cluster information to about hotspots
# and are behavior by classifying the different cluster type i.e clumped, dispersed, random. 
import csv
import arcpy

print("Data Input from Modis Forest Fire Occurences")
print()
print("Please input your boundary Shapefile for area of analysis")
print()
input("")

def main():
    File = open (r"userInputFlie.csv", "r")
    datafile = csv.reader(File, skip_blank_lines = True )

    # newfile = open (r"exported_data.csv", "w")
    # writer = csv.writer(newfile)

    # header = next(datafile)
    # writer.writerow(header+["", ""])
print("************************************************************************")
#*************************************************************
print ("Enter values below") 
print ("*******************************************************************") 
print()
minFeat = float(input("Please state a minimum number of features to include in your clusters:  ")
print()
clumped = float(input("Please enter search distance for a clumped cluster:  ")
print()
dispersed = float(input("Please enter distance for a dispersed cluster:  ")
print()
year = input("Please enter year you would like analyzed:   ")
print()
end = input("Do you want to stop entering values (Y/N)?:  ")
        print()
        if  end.upper() == 'Y' :
            break

print("************************************************************************")



arcpy.env.overwriteOutput = True

firePointsTable = r"C:\GEOM67\GroupProject\BC_fire_points_2019.csv"

arcpy.management.XYTableToPoint(firePointsTable, r"C:\GEOM67\GroupProject\firePoints.shp", 
"longitude", "latitude","","")      # optional parameters: {z_field}, {coordinate_system})

points = r"C:\GEOM67\GroupProject\firePoints.shp"

arcpy.stats.DensityBasedClustering(points, r"C:\GEOM67\GroupProject\pointClusters.shp", 
"HDBSCAN", 15) 
# addiotnal parameters for DBSCAN and OPTICS: ({search_distance}, cluster_sensitivity)




print ("Outputs for Forest fire occurrences in your region:  ") 
# print columns 
print()
print("Cluster Data: ")
# print columns
print()

print("Total amount of clusterd points clumped", clumpedData " and total dispersed", dispersedData )
print("Number of areas and points analyed over", inputyear "years in", inputRegion "region")
print()
print("************************************************************************")
print("Download the new shapefile with all you clustered data: ")

aprx.saveACopy(r"userOutputData.lyrx")

answer = input("Would you like to upload another file? Y for Yes OR N for No?:  ")

    if answer.upper() == "Y" :        
        break