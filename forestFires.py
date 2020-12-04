# Program Purpose
# This program will allow the user to evaluate forest fire activity in the region chosen. 
# You Will upload a CSV file, the program will output cluster information to about hotspots
# and are behavior by classifying the different cluster type i.e clumped, dispersed, random. 
import csv
import arcpy
# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

print("Data Input from Modis Forest Fire Occurences")
print()
print("Please input your boundary csv file for area analysis")
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



# arcpy.env.overwriteOutput = True

firePointsTable = r"C:\GEOM67\GroupProject\BC_fire_points_2019.csv"

arcpy.management.XYTableToPoint(firePointsTable, r"C:\GEOM67\GroupProject\firePoints.shp", 
"longitude", "latitude","","")      # optional parameters: {z_field}, {coordinate_system})

points = r"C:\GEOM67\GroupProject\firePoints.shp"

arcpy.stats.DensityBasedClustering(points, r"C:\GEOM67\GroupProject\pointClusters.shp", 
"HDBSCAN", 15) 
# additonal parameters for DBSCAN and OPTICS: ({search_distance}, cluster_sensitivity)

#Left to do 

#SELECT points contained within the boundary area of interest

#CREATE clusters of the points contained within the area using Density

#based Clustering geoprocessing tool (Multi-scale (OPTICS) method) using first cluster distance

#CREATE clusters within each area using Density-based Clustering geoprocessing tool using second cluster distance

#REPEAT for each area of interest

#CLASSIFY clusters based on outputs, specified cluster distance

#RECLASSIFY nosie values as random points


print ("Outputs for Forest fire occurrences in your region:  ") 
# print columns 
print()
print("Cluster Data: ")
# print columns
print()

#DISPLAY type, number of point clumps within each area (table and/or map), number of points in each cluster, number of random points

print("Total amount of clustered points clumped", clumpedData " and total dispersed", dispersedData )
print("Number of areas and points analyed over", inputyear "years in", inputRegion "region")
print()
print("************************************************************************")
print("A shapefile with all your clustered data will be downloaded: ")



#tell user where to find there shapefile
#aprx.saveACopy(r"userOutputData.lyrx")
#lyt.exportToPDF

answer = input("Would you like to upload another file? Y for Yes OR N for No?:  ")

    if answer.upper() == "Y" :        
        break





# how to count number of total ID's (if loop)
# print out csv file
# shape files will output to workspace

# Work on dictionary for provices and territroies 