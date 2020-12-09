import arcpy, csv, os, sys


arcpy.env.overwriteOutput = True

# User input for output file path (added by Aaron Dec. 9, 2020)
while True:
    outWorkspace = str(input("Please enter the file path you wish to store your outputs in (e.g. r\"C:\GEOM67\"): "))
    try:
        outWorkspace = open(prompt, 'r').readlines()
    except FileNotFoundError:
        print("Wrong file path")
    else:
        break

outWorkspace = outWorkspace.rstrip('"')
outWorkspace = outWorkspace.rstrip("'")

print(outWorkspace)
# User input for the fire points csv file (added by Aaron Dec. 9, 2020)
 def firePointsTable (shp,shx,dbf): #Add by Michelle
    firePointsTable = str(input("Please enter the file path to the 'modis_2019_Canada.csv' file (e.g. r\"C:\GEOM67\modis_2019_Canada.csv\"): "))
    if self.shp or self.dbf:        
            self.load()
        else:
            raise ShapefileException("Shapefile Reader requires a shapefile or file-like object.")


firePointsTable = firePointsTable.rstrip('"')
firePointsTable = firePointsTable.rstrip("'")


# User input for the census tracts shapefile file path (added by Aaron Dec. 9, 2020)
census_tracts = str(input("Please enter the file path to the 'lpr_000b16a_e.shp' file (e.g. r\"C:\GEOM67\lpr_000b16a_e.shp\"): ")) 

census_tracts = census_tracts.rstrip('"')
census_tracts = census_tracts.rstrip("'")



# converting the csv modis file into a point shapefile (added by Aaron Dec. 9, 2020)
arcpy.management.XYTableToPoint(firePointsTable, outWorkspace + "\{}irePoints.shp".format("f"), 
"longitude", "latitude","","")             # optional parameters: {z_field}, {coordinate_system})

# assigning the fire point shapefile to a variable (added by Aaron Dec. 9, 2020)
points = outWorkspace + "\{}irePoints.shp".format("f")


# Below is a dictionary holding province name values. (added by Aaron Dec. 4, 2020)
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

# while loop that lets the user input as many provinces/territories they want to analyze (added by Aaron Dec. 4, 2020)
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
# this loop iterates through each inputted province/territory name and abbreviation (added by Aaron Dec. 4, 2020)
for region, ab in zip(study_area, abbr): # a shapefile of each inputted province/territory is created
    arcpy.Select_analysis(census_tracts, outWorkspace + '\{}ound{}.shp"'.format(b, ab),
    "PRNAME = '{}'".format(region)) # each output will have its province/territory abbrevation at the end  
    


# each previous clipped province/territory is then used to clip the fire points (added by Aaron Dec. 4, 2020)
for ab in abbr:
    arcpy.Clip_analysis(points, outWorkspace + '\{}ound{}.shp"'.format(b, ab),
    outWorkspace + '\clipped_points_{}.shp"'.format(ab))
# each output will have its province/territory abbrevation at the end


# user is asked to input the min amount of features to clipped for each analysis (added by Aaron Dec. 4, 2020)
minFeatures1 = float(input("Please enter the minimum amount of features for the clumped cluster analysis: "))
print()
minFeatures2 = float(input("Please enter the minimum amount of features for the dispersed cluster analysis: "))
print()
srcDistance1 = input("Please enter the kilometer search distance for identifying clumped clusters: ") + " Kilometers"
srcDistance2 = input("Please enter the kilometer search distance for identifying dispersed clusters (must be larger than first search distance): ") + " Kilometers"
print()

# Clumped cluster (added by Aaron Dec. 4, 2020)
# For loop iterates for each inputted province's/territory's clipped fire points
for ab in abbr:
    arcpy.stats.DensityBasedClustering(outWorkspace + '\clipped_points_{}.shp"'.format(ab), 
    outWorkspace + '\Clumped_Cluster_{}.shp"'.format(ab), 
    "OPTICS", minFeatures1, srcDistance1, "") 

# Dispersed cluster
# For loop iterates for each input province/territory clipped fire points

for ab in abbr: 
    arcpy.Select_analysis(outWorkspace + '\Clumped_Cluster_{}.shp"'.format(ab), outWorkspace + '\Dispersed_Input_{}.shp"'.format(ab),'"CLUSTER_ID" = -1')

for ab in abbr:
    arcpy.stats.DensityBasedClustering(outWorkspace + '\Dispersed_Input_{}.shp"'.format(ab), 
    outWorkspace + '\Dispersed_Cluster_{}.shp"'.format(ab),
    "OPTICS", minFeatures2, srcDistance2, "")

for ab in abbr: 
    arcpy.Select_analysis(outWorkspace + '\Dispersed_Cluster_{}.shp"'.format(ab), outWorkspace + '\Random_Points{}.shp"'.format(ab),'"CLUSTER_ID" = -1')

tableList = arcpy.ListTables
for dbaseTable in tableList(): # check if there is a way to only select certain tables - don't need inputs, just outputs
    if "Random_points" in tableList():
        outTable = os.path.join(outWorkspace, os.path.splitext(dbaseTable)[0])
        arcpy.CopyRows_management(dbaseTable, outTable.csv)
    else: 
        print("Table could not be found.")

# try excepts: arcgisscripting.ExecuteError: ERROR 110141: The Minimum Number of Features per Cluster is greater than the number of features in the dataset.Failed to execute (DensityBasedClustering).

# these files can then be read back in and counted for the results ie. 
print("************************************************************************")

total_random_points = []
total_clumped_clusters = []
total_dispersed_clusters = []

with open(file_path + "random_point_rows.csv","r") as csv_file: # wasn't recognizing file in same folder, had to add file path
    csv_reader = csv.reader(csv_file, delimiter=',') 
for lines in csv_reader: 
    total_random_points.append(lines[2]) # third field in table, should be list index 2? 

#added by Michelle
print("************************************************************************")
print(" You total number of random points is ")
print(len(total_random_points)

# determine whether user wants to enter another set of input values
end = input("Do you want to stop entering values (Y/N)? ")
print()
if  end.upper() == 'Y' :
    break


# #added by Michelle
# except arcpy.ExecuteError:
#     print(arcpy.GetMessages(2))  

# except Exception:
#     e = sys.exc_info()[1]
#     print(e.args[0])
#     arcpy.AddError(e.args[0])
# else:
#     print ("Something")
