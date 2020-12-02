# PSPGroup
Programming group project

PROGRAM Determine_Cluster_Type_Forest_Fires

DISPLAY program’s purpose - classify forest fire clusters (clumped,
dispersed, random)

DISPLAY prompt for user input

GET forest fire data from user

GET boundary shapefile for areas to be analyzed from user

CHECK if file extensions match the file types needed for analysis

READ user input file

DISPLAY prompt for user to input parameters for density analysis

GET parameters for cluster analysis: minimum features, cluster distance,
cluster sensitivity

CONVERT CSV table to vector point layer

SELECT points contained within the boundary area of interest

CREATE clusters of the points contained within the area using Density

based Clustering geoprocessing tool (Multi-scale (OPTICS) method) using
first cluster distance

CREATE clusters within each area using Density-based Clustering
geoprocessing tool using second cluster distance
REPEAT for each area of interest

CLASSIFY clusters based on outputs, specified cluster distance

RECLASSIFY nosie values as random points

DISPLAY output message, including number of points analyzed, number
of areas

DISPLAY type, number of point clumps within each area (table and/or map), number of
points in each cluster, number of random points

END PROGRAM