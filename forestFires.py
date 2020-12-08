# Program Purpose
# This program will allow the user to evaluate forest fire activity in the region chosen. 
# You Will upload a CSV file, the program will output cluster information to about hotspots
# and are behavior by classifying the different cluster type i.e clumped, dispersed, random. 

import csv
import arcpy

print("Data Input from Modis Forest Fire Occurences")
print()
print("Please input your boundary csv file for area analysis")
print()
input("")

def main():
    File = open (r"userInputFlie.csv", "r")
    datafile = csv.reader(File, skip_blank_lines = True )

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
year = input(str("Please enter year you would like analyzed:   "))
print()
end = input("Do you want to stop entering values (Y/N)?:  ")
        print()
        if  end.upper() == 'Y' :
            break

print("************************************************************************")


#change to user input
firePointsTable = r"C:\GEOM67\GroupProject\modis_2019_Canada.csv"

# converting the csv modis file into a point shapefile
arcpy.management.XYTableToPoint(firePointsTable, r"C:\GEOM67\GroupProject\firePoints.shp", 
"longitude", "latitude","","")             # optional parameters: {z_field}, {coordinate_system})

# assigning the fire point shapefile to a variable
points = r"C:\GEOM67\GroupProject\firePoints.shp"

# Canada census tract province and territory boundary shapefile 
census_tracts = r"C:\GEOM67\GroupProject\lpr_000b16a_e\lpr_000b16a_e.shp"

# Below is a dictionary holding province name values.
# The first value of each key represents the values as exactly written in the PRNAME field in the 
# census tracts file. The second value of each key is the abbrevation of those names which will 
# be used for file names during the arcpy geoprocessing below.
provinces_territories = {1:('Newfoundland and Labrador / Terre-Neuve-et-Labrador', 'NL'), 
2:("Prince Edward Island / Île-du-Prince-Édouard", "PE"),
3:("Nova Scotia / Nouvelle-Écosse", "NS"), 4:("New Brunswick / Nouveau-Brunswick", "NB"), 
5:("Quebec / Québec","QC") , 6:("Ontario", "ON"), 7:("Manitoba", "MB"), 8:("Saskatchewan", "SK"),
 9:("Alberta", "AB"), 10:("British Columbia / Colombie-Britannique", "BC"),
11:("Yukon", "YT"), 12:("Northwest Territories / Territoires du Nord-Ouest", "NT"), 13:("Nunavut", "NU")}

# printing the above dictionary for the user to see
print(provinces_territories)

# creating an empty list to hold inputted province names (from dictionary)
study_area = []
# creating an empty list to hold inputted province name abbreviations (from dictionary)
abbr = []

# while loop that lets the user input as many provinces/territories they want to analyze
while True:
    provTer = float(input("Please enter the number corresponding to the province/territory you want to analyze: "))
    study_area.append(provinces_territories[provTer][0]) # Province name from dictionary is appended to study_area
    abbr.append(provinces_territories[provTer][1]) # Province abbreviation is appended to abbr

    print() # User has option to enter more provinces for analysis
    end = input("Do you want to enter another province/territory to analyze (Y/N)? ")
    print()
    if end.upper() == 'N' :
        break

print(study_area)

# source for looping two lists simultaneously: https://stackoverflow.com/questions/1663807/how-to-iterate-through-two-lists-in-parallel
# this loop iterates through each inputted province/territory name and abbreviation
for region, ab in zip(study_area, abbr): # a shapefile of each inputted province/territory is created
    arcpy.Select_analysis(census_tracts, r"C:\GEOM67\GroupProject\bound{}.shp".format(ab),
    "PRNAME = '{}'".format(region)) # each output will have its province/territory abbrevation at the end  

# each previous clipped province/territory is then used to clip the fire points
for ab in abbr:
    arcpy.Clip_analysis(points, r"C:\GEOM67\GroupProject\bound{}.shp".format(ab),
    r"C:\GEOM67\GroupProject\clipped_points_{}.shp".format(ab))
# each output will have its province/territory abbrevation at the end
# user is asked to input the min amount of features to clipped for each analysis
minFeatures1 = float(input("Please enter the minimum amount of features for the clumped cluster analysis: "))
minFeatures2 = float(input("Please enter the minimum amount of features for the dispersed cluster analysis: "))

# Clumped cluster
# For loop iterates for each inputted province's/territory's clipped fire points
for ab in abbr:
    arcpy.stats.DensityBasedClustering(r"C:\GEOM67\GroupProject\clipped_points_{}.shp".format(ab), 
    r"C:\GEOM67\GroupProject\Clumped_Cluster_{}.shp".format(ab), 
    "OPTICS", minFeatures1, "20 Kilometers", "") 

# Dispersed cluster
# For loop iterates for each inputted province's/territory's clipped fire points
for ab in abbr:
    arcpy.stats.DensityBasedClustering(r"C:\GEOM67\GroupProject\clipped_points_{}.shp".format(ab), 
    r"C:\GEOM67\GroupProject\Dispersed_Cluster_{}.shp".format(ab),
     "OPTICS", minFeatures2, "30 Kilometers", "")

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