import arcpy, csv

try: 
    # To allow overwriting the outputs change the overwrite option to true.
    arcpy.env.overwriteOutput = True

    # Hard Coded CSV document 
    firePointsTable = "modis_2019_Canada.csv"

    # converting the csv modis file into a point shapefile 
    arcpy.management.XYTableToPoint(firePointsTable, "output\canadafirepoints.shp", 
    "longitude", "latitude","","")   

    # assigning the fire point shapefile to a variable 
    points = "output\canadafirepoints.shp"

    # Canada census tract province and territory boundary shapefile 
    census_tracts = "lpr_000b16a_e\lpr_000b16a_e.shp"

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
        arcpy.Select_analysis(census_tracts, "output\{}ound{}.shp".format("b", ab),
        "PRNAME = '{}'".format(region)) # each output will have its province/territory abbrevation at the end  
        
    
    # each previous clipped province/territory is then used to clip the fire points
    for ab in abbr:
        arcpy.Clip_analysis(points, "output\{}ound{}.shp".format("b", ab),
        "output\clipped_points_{}.shp".format(ab))
    # each output will have its province/territory abbrevation at the end

    # user is asked to input the min amount of features to clipped for each analysis
    minFeatures1 = float(input("Please enter the minimum amount of features for the clumped cluster analysis: "))
    minFeatures2 = float(input("Please enter the minimum amount of features for the dispersed cluster analysis: "))

    srcDistance1 = input("Please enter the kilometer search distance for identifying clumped clusters: ") + " Kilometers"
    srcDistance2 = input("Please enter the kilometer search distance for identifying dispersed clusters (must be larger than first search distance): ") + " Kilometers"

    # Clumped cluster
    # For loop iterates for each inputted province's/territory's clipped fire points
    for ab in abbr:
        print("Creating a clumped cluster shapefile for", ab)
        arcpy.stats.DensityBasedClustering("output\clipped_points_{}.shp".format(ab), 
        "output\Clumped_Cluster_{}.shp".format(ab), 
        "OPTICS", minFeatures1, srcDistance1, "") 

    # Dispersed cluster
    # For loop iterates for each input province/territory clipped fire points

    for ab in abbr: 
        arcpy.Select_analysis("output\Clumped_Cluster_{}.shp".format(ab),"output\Dispersed_Input_{}.shp".format(ab), '"CLUSTER_ID" = -1')

    for ab in abbr:
        print("Creating a dispersed cluster shapefile for: ", ab)
        arcpy.stats.DensityBasedClustering("output\Dispersed_Input_{}.shp".format(ab), 
        "output\Dispersed_Cluster_{}.shp".format(ab),
        "OPTICS", minFeatures2, srcDistance2, "")

    for ab in abbr: 
        arcpy.Select_analysis("output\Dispersed_Cluster_{}.shp".format(ab),"output\Random_Points{}.shp".format(ab),'"CLUSTER_ID" = -1')

    print()
    print("************************************************************************")
    print("A shapefile with all your clustered data will be downloaded: ")
    print()


except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))  
    # Handle the code somehow
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])
except:
    print("An Error has occurred")
