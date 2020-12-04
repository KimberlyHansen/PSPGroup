canada = ["Provinces", "Territories"]
directory = canada

Provinces = ["Ontario", "Quebec", "Newfoundland and Labrador", "New Brunswick", "Nova Scotia", "Prince Edward Island", "Manitoba", "Saskatchewan", "Alberta", "British Columbia"]
Territories = ["Yukon", "Northwest Territories", "Nunavut"]
directoryOptions = []
directoryOptions.append(Provinces)
directoryOptions.append(Territories)

menudirectory = {}

menudirectory.update({"Provinces": Provinces})
menudirectory.update({"Territories" : Territories})
print(menudirectory)

PickCategory = input(str("Please pick any category by entering either Province OR Territory :  "))
print("The category selected is " +PickCategory)

if PickCategory == "Province":
    x = menudirectory.get("Provinces")
    print(x)
elif PickCategory == "Territory":
    x = menudirectory.get("Territories")
    print(x)

else:
    print("ERROR")

Choice = input(str("Please pick any category listed :"))
print("The chosen category is " +Choice)