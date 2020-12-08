import arcpy, csv, os, sys

try: 
    arcpy.env.overwriteOutput = True

    # Set local variables for output workspace, results geodatabase
    outWorkspace = r"C:\GEOM67\GroupProject"
    outGDB = "results.gdb"

    # Create's the file geodatabase
    arcpy.CreateFileGDB_management(outWorkspace, outGDB)

    firePointsTable = r"C:\GEOM67\GroupProject\modis_2019_Canada.csv"

    # converting the csv modis file into a point shapefile
    arcpy.management.XYTableToPoint(firePointsTable, r"C:\GEOM67\GroupProject\firePoints.shp", 
    "longitude", "latitude","","")   
    # optional parameters: {z_field}, {coordinate_system}) We could have this
    # Coordinate_System = arcpy.GetParameterAsText(2) or ""
    #   if Coordinate_System == "Unknown":
    #           print("{2} has an unknown Coordinate system".format(fc))
    #   else:
    #           print("{2}".format(fc, Coordinate_System))

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

    srcDistance1 = input("Please enter the kilometer search distance for identifying clumped clusters: ") + " Kilometers"
    srcDistance2 = input("Please enter the kilometer search distance for identifying dispersed clusters (must be larger than first search distance): ") + " Kilometers"


    # Clumped cluster
    # For loop iterates for each inputted province's/territory's clipped fire points
    for ab in abbr:
        arcpy.stats.DensityBasedClustering(r"C:\GEOM67\GroupProject\clipped_points_{}.shp".format(ab), 
        r"C:\GEOM67\GroupProject\Clumped_Cluster_{}.shp".format(ab), 
        "OPTICS", minFeatures1, srcDistance1, "") 

    # Dispersed cluster
    # For loop iterates for each input province/territory clipped fire points

    for ab in abbr: 
        arcpy.Select_analysis(r'C:\GEOM67\GroupProject\Clumped_Cluster_{}.shp'.format(ab),r'C:\GEOM67\GroupProject\Dispersed_Input_{}.shp'.format(ab),'"CLUSTER_ID" = -1')

    for ab in abbr:
        arcpy.stats.DensityBasedClustering(r"C:\GEOM67\GroupProject\Dispersed_Input_{}.shp".format(ab), 
        r"C:\GEOM67\GroupProject\Dispersed_Cluster_{}.shp".format(ab),
        "OPTICS", minFeatures2, srcDistance2, "")

    for ab in abbr: 
        arcpy.Select_analysis(r'C:\GEOM67\GroupProject\Dispersed_Cluster_{}.shp'.format(ab),r'C:\GEOM67\GroupProject\Random_Points{}.shp'.format(ab),'"CLUSTER_ID" = -1')

    tableList = arcpy.ListTables
    for dbaseTable in tableList(): # check if there is a way to only select certain tables - don't need inputs, just outputs
        if "Random_points" in tableList():
            outTable = os.path.join(outWorkspace, os.path.splitext(dbaseTable)[0])
            arcpy.CopyRows_management(dbaseTable, outTable.csv)
        else: 
            print("Table could not be found.")

    # try excepts: arcgisscripting.ExecuteError: ERROR 110141: The Minimum Number of Features per Cluster is greater than the number of features in the dataset.Failed to execute (DensityBasedClustering).
    
    # these files can then be read back in and counted for the results ie. 

    total_random_points = []
    total_clumped_clusters = []
    total_dispersed_clusters = []

    with open(file_path + "random_point_rows.csv","r") as csv_file: # wasn't recognizing file in same folder, had to add file path
        csv_reader = csv.reader(csv_file, delimiter=',') 
    for lines in csv_reader: 
        total_random_points.append(lines[2]) # third field in table, should be list index 2? 

    print(len(total_random_points))
    

except:
    print("An Error has occurred")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))  
    # Handle the code somehow
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])
finally:
    print ("Something")
