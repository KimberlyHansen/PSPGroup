import arcpy

#geodatabase model
arcpy.env.workspace = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Cluster_Analysis_Model.gdb"

#variables used in model - these need to be set up as user inputs 
in_table = r"C:\GEOM67_Program\GroupProject2\Fire_Cluster_Analysis_Model\Fire_Points_Canada_2019.csv"
out_feature_class = "Fire_Points"
x_field = "latitude"
y_field = "longitude"
coordinate_system = "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

#running the conversion to table 
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field,"",coordinate_system)

print("Points converted to table.")
#output shapefile has lat/long, etc. but only showing a few points on the map - take up with Karen later 
