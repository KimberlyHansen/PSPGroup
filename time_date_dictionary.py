month = input("Please enter the month (2019) you are interested in analyzing: ")


month_range = {
 'January':("acq_date >= timestamp '2019-01-01' And acq_date <= timestamp '2019-01-31'"), 
'February':("acq_date >= timestamp '2019-02-01' And acq_date <= timestamp '2019-02-28'"),
'March':("acq_date >= timestamp '2019-03-01' And acq_date <= timestamp '2019-03-31'"),
 'April':("acq_date >= timestamp '2019-04-01' And acq_date <= timestamp '2019-04-30'"), 
'May':("acq_date >= timestamp '2019-05-01' And acq_date <= timestamp '2019-05-31'") , 
'June':("acq_date >= timestamp '2019-06-01' And acq_date <= timestamp '2019-06-30'"),
 'July':("acq_date >= timestamp '2019-07-01' And acq_date <= timestamp '2019-07-31'"), 
 'August':("acq_date >= timestamp '2019-08-01' And acq_date <= timestamp '2019-08-31'"),
 'September':("acq_date >= timestamp '2019-09-01' And acq_date <= timestamp '2019-09-30'"),
  'October':("acq_date >= timestamp '2019-10-01' And acq_date <= timestamp '2019-10-31'"),
'November':("acq_date >= timestamp '2019-11-01' And acq_date <= timestamp '2019-11-30'"), 
'December':("acq_date >= timestamp '2019-12-01' And acq_date <= timestamp '2019-12-31'")}


time = []
month_name = []

for ab in abbr:
     = float(input("Please enter the month you want to analyze: "))
    month_name.append(month) # month name appended to month_name
    time.append(month_range[month]) # Month time range from dictionary is appended to time
    
    print() # User has option to enter more months for analysis
    end = input("Do you want to enter another month to analyze (Y/N)? ")
    print()
    if end.upper() == 'N' :
        break


for region, ab in zip(study_area, abbr): # a shapefile of each inputted province/territory is created
    arcpy.Select_analysis(census_tracts, r"C:\GEOM67\GroupProject\bound{}.shp".format(ab),
    "PRNAME = '{}'".format(region)) # each output will have its province/territory abbrevation at the end  

# each previous clipped province/territory is then used to clip the fire points
for ab in abbr:
    arcpy.Clip_analysis(points, r"C:\GEOM67\GroupProject\bound{}.shp".format(ab),
    r"C:\GEOM67\GroupProject\clipped_points_{}.shp".format(ab))
# each output will have its province/territory abbrevation at the end


for month in month_range: # a shapefile of each selected month is created
    arcpy.Select_analysis(r"C:\GEOM67\GroupProject\clipped_points_{}.shp", 
    r"C:\GEOM67\GroupProject\clipped_points_{}_{}.shp".format(ab, month),
    {}.format(region)) # each output will have its province/territory abbrevation at the end  


arcpy.Select_analysis(in_features=Fire_Points_From_Table, out_feature_class=Fire_Points_TimeFrame, where_clause=Time_Range)



acq_date >= timestamp '2019-12-01' And acq_date <= timestamp '2019-12-31'

for key 1 in dictionary --> "acq_date <= [list element 1]' And acq_date >= [list element 2]" 

# Process: Select (2)
arcpy.Select_analysis(in_features=Fire_Points_From_Table, out_feature_class=Fire_Points_TimeFrame, where_clause=Time_Range)

Time_Range = arcpy.GetParameterAsText(3) or " "