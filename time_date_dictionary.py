month = input("Please enter the month (2019) you are interested in analyzing: ")


month_range = {'January':("timestamp '19-1-1 00:00:00'","timestamp '19-1-31' 23:59:59"), 
'February':("timestamp '19-2-1 00:00:00'","timestamp '19-2-28' 23:59:59"),
'March':("timestamp '19-3-1 00:00:00'","timestamp '19-3-31' 23:59:59"), 'April':("timestamp '19-4-1 00:00:00'","timestamp '19-4-30' 23:59:59"), 
'May':("timestamp '19-5-1 00:00:00'","timestamp '19-5-31' 23:59:59") , 'June':("timestamp '19-6-1 00:00:00'","timestamp '19-6-30' 23:59:59"), 'July':("timestamp '19-7-1 00:00:00'","timestamp '19-7-31' 23:59:59"), 'August':("timestamp '19-8-1 00:00:00'","timestamp '19-8-31' 23:59:59"),
 'September':("timestamp '19-9-1 00:00:00'","timestamp '19-9-30' 23:59:59"), 'October':("timestamp '19-10-1 00:00:00'","timestamp '19-10-31' 23:59:59"),
'November':("timestamp '19-1-1 00:00:00'","timestamp '19-1-30' 23:59:59"), 'December':("timestamp '19-12-1 00:00:00'","timestamp '19-12-31' 23:59:59")}

for key 1 in dictionary --> "acq_date <= [list element 1]' And acq_date >= [list element 2]" 

# Process: Select (2)
arcpy.Select_analysis(in_features=Fire_Points_From_Table, out_feature_class=Fire_Points_TimeFrame, where_clause=Time_Range)

Time_Range = arcpy.GetParameterAsText(3) or " "
