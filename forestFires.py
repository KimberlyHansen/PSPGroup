#Program Purpose
#This program will allow the user to evaluate forest re activity in the region chosen. You Will upload a CSV le, the program will output cluster information to about hotspots and re behavior by classifying the dierent cluster type i.e clumped, dispersed, random. 
import csv

print("Data Input from Modis Forest Fire Occurences")
print()
print("Please input your boundary Shapefile for area of analysis")
print()
input("")

def main():
    Flie = open (r"blah.csv", "r")
    datafile = csv.reader(Flie)

    newfile = open (r"exported_data.csv", "w")
    writer = csv.writer(newfile)

    header = next(datafile)
    writer.writerow(header+["", ""])