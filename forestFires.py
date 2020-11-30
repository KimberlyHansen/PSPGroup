#Program Purpose
#This program will allow the user to evaluate forest re activity in the region chosen. You Will upload a CSV le, the program will output cluster information to about hotspots and re behavior by classifying the dierent cluster type i.e clumped, dispersed, random. 
import csv
import arcpy

print("Data Input from Modis Forest Fire Occurences")
print()
print("Please input your boundary Shapefile for area of analysis")
print()
input("")

def main():
    File = open (r"blah.csv", "r")
    datafile = csv.reader(File)

    newfile = open (r"exported_data.csv", "w")
    writer = csv.writer(newfile)

    header = next(datafile)
    writer.writerow(header+["", ""])

#*************************************************************

print("Please state a minimum number of features to include in your clusters:  ")
input()
print()
print("Please enter search distance for a clumped cluster:  ")
input()
print()
print("Please enter distance for a dispersed cluster:  ")
input()
print()
print("Please enter year you would like analyzed:   ")
input()
print()
end = input("Do you want to stop entering values (Y/N)? ")
        print()
        if  end.upper() == 'Y' :
            break
#*************************************************************
