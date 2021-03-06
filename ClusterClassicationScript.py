# -*- coding: utf-8 -*-
"""Generated by ArcGIS ModelBuilder on: 2020-12-03 14:44:14
All ModelBuilder functionality may not be exported. Edits may be required for equivalency with the original model.
"""

#Course components to include: 
#repetition - repeat files, or for ____ in ____ --> tool - maybe also to count outputs? 
#modularization - programmer-defined functions - one for each ArcPy tool -- make sure it's functioning! 
#string manipulation - ? 
#selection - use IF features and booleans to select random/clumped/dispersed
#read input files, write to table from Arc 
#package all files into one folder? 
import arcpy, csv

file_path = input("Please enter the file pathway in which you want to store the output geodatabase and csv files: ")
#this file path needs to have forward slashes, unless we figure out a way to make r" work depending on the structure of the filepath


# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

# Script parameters
Boundary_Shapefile = arcpy.GetParameterAsText(0) or ""

Input_CSV_Table = arcpy.GetParameterAsText(1) or ""
Coordinate_System = arcpy.GetParameterAsText(2) or ""
Time_Range = arcpy.GetParameterAsText(3) or " "
Location = arcpy.GetParameterAsText(4) or " "
Clumped_Cluster_Distance = arcpy.GetParameterAsText(5) or " "
Dispersed_Cluster_Distance = arcpy.GetParameterAsText(6) or " "

if Coordinate_System == "Unknown":
        print("{2} has an unknown Coordinate system".format(fc))

else:
        print("{2}".format(fc, Coordinate_System))
    
# Local variables:
Fire_Points_From_Table = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Fire_Points_From_Table"
Fire_Points_TimeFrame = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Fire_Points_TimeFrame"
Area_Selection = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Area_Selection"
Fire_Points_Range_Clip = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Fire_Points_Area_Clip"
String__Multi_scale__OPTICS__Clustering__2_ = "OPTICS"
Clumped_Clusters = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Clumped_Clusters"
SQL_Expression__5_ = "CLUSTER_ID = -1"
Dispersed_Input = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Dispersed_Input"
String__Multi_scale__OPTICS__Clustering = "OPTICS"
Dispersed_Clusters = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Dispersed_Clusters"
SQL_Expression__3_ = "CLUSTER_ID = -1"
Random_Points = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb\Random_Points"

# Process: XY Table To Point
tempEnvironment0 = arcpy.env.outputCoordinateSystem
arcpy.env.outputCoordinateSystem = "Coordinate System"
arcpy.XYTableToPoint_management(in_table=Input_CSV_Table, out_feature_class=Fire_Points_From_Table, x_field="longitude", y_field="latitude", z_field="", coordinate_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
arcpy.env.outputCoordinateSystem = tempEnvironment0

# Process: Select (2)
arcpy.Select_analysis(in_features=Fire_Points_From_Table, out_feature_class=Fire_Points_TimeFrame, where_clause=Time_Range)

# Process: Select
arcpy.Select_analysis(in_features=Boundary_Shapefile, out_feature_class=Area_Selection, where_clause=Location)

# Process: Clip
arcpy.Clip_analysis(in_features=Fire_Points_TimeFrame, clip_features=Area_Selection, out_feature_class=Fire_Points_Range_Clip, cluster_tolerance="")

# Process: Density-based Clustering (2)
# tempEnvironment0 = arcpy.env.outputZFlag
# tempEnvironment0 = arcpy.env.outputZFlag
arcpy.DensityBasedClustering_stats(in_features=Fire_Points_Range_Clip, output_features=Clumped_Clusters, cluster_method=String__Multi_scale__OPTICS__Clustering__2_, min_features_cluster="5", search_distance=Clumped_Cluster_Distance, cluster_sensitivity="")
arcpy.env.outputZFlag = tempEnvironment0

# Process: Select (4)
arcpy.Select_analysis(in_features=Clumped_Clusters, out_feature_class=Dispersed_Input, where_clause=SQL_Expression__5_)

# Process: Density-based Clustering
tempEnvironment0 = arcpy.env.outputZFlag
tempEnvironment0 = arcpy.env.outputZFlag
arcpy.DensityBasedClustering_stats(in_features=Dispersed_Input, output_features=Dispersed_Clusters, cluster_method=String__Multi_scale__OPTICS__Clustering, min_features_cluster="5", search_distance=Dispersed_Cluster_Distance, cluster_sensitivity="")
arcpy.env.outputZFlag = tempEnvironment0

# Process: Select (5)
arcpy.Select_analysis(in_features=Dispersed_Clusters, out_feature_class=Random_Points, where_clause=SQL_Expression__3_)

# Export shapefile tables to csv's that can be worked with 
outWorkspace = "c:/CSV_Results"

tableList = arcpy.ListTables
for dbaseTable in tableList: # check if there is a way to only select certain tables - don't need inputs, just outputs
  outTable = os.path.join(outWorkspace, os.path.splitext(dbasetable)[0])
  arcpy.CopyRows_management(dbaseTable, outTable.csv) 
  
# these files can then be read back in and counted for the results ie. 

total_random_points = []

with open(file_path + "random_point_rows.csv","r") as csv_file: # wasn't recognizing file in same folder, had to add file path
  csv_reader = csv.reader(csv_file, delimiter=',') 
  for lines in csv_reader: 
    total_random_points.append(lines[2]) # third field in table, should be list index 2? 

print(len(total_random_points))


