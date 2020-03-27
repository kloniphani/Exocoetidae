#Object Oriented Classes
from Roommates.StableRoommates import *;
from Clustering.Distribution import *;

#Third Party Classes
from numpy import * 
from geopy import distance #Geo Location
import json, io, datetime, progressbar, csv
from xml.etree import ElementTree

firstList =  []
secondList = [] 

#Reading Json files to populate the list 
#NODES
FileName = ".\Source\Data\Study\Soweto.json"
with io.open(FileName, 'r', encoding="utf-8") as JsonData:
    JsonGeoData = json.load(JsonData)
    ResidualEnergies, SNRs = Distribution.Normal() # Random Values
    
    print("\nCreating Nodes.")
    for k, value in JsonGeoData.items():
        firstList.append({"name": k, 
                          "residual": random.choice(ResidualEnergies), 
                          "snr": random.choice(SNRs),
                          "pos": (value["geometry"]["location"]['lat'], value["geometry"]["location"]['lng'])})

#USERS
FileName = ".\Source\Data\Health Centers\Soweto.json"
with io.open(FileName, 'r', encoding="utf-8") as JsonData:
    JsonGeoData = json.load(JsonData)
    BDs = random.normal(10, 2.1, 100000000)

    print("Creating Users.")
    for k, value in JsonGeoData.items():
        secondList.append({"name": k,
                           "bandwidwith": random.choice(BDs),
                           "pos": (value["geometry"]["location"]['lat'], value["geometry"]["location"]['lng'])})

print("Computing Preferences.")
#Computing preferences
def Distance(node, user):
    return distance.distance(node["pos"], user["pos"]).kilometers

#NODES
for node in firstList:
    preferences = []
    for user in secondList:
        if Distance(node, user) <= 5:
            preferences.append(user["name"])
    node["preferences"] = preferences;
 

#USERS
Average_Residual = average([(node["residual"]) for node in firstList])
Average_SNR = average([node["snr"] for node in firstList])

for user in secondList:
    preferences = []
    for node in firstList:
        if node["snr"] >= Average_SNR and node["residual"] >= Average_Residual:
            preferences.append(node["name"])
    user["preferences"] = preferences;


"""
firstList = [{"name":'A',"age":40,"preferences":['U','V','W','X','Y','Z']},
                 {"name":'B',"age":21,"preferences":['V','W','Y','U','X','Z']},
                 {"name":'C',"age":30,"preferences":['V','W','U','Y','X','Z']},
                 {"name":'D',"age":50,"preferences":['V','W','U','Y','X','Z']},
                 {"name":'E',"age":28,"preferences":['U','W','V','Y','X','Z']},
                 {"name":'F',"age":28,"preferences":['V','W','U','Y','X','Z']}
            ]

secondList = [{"name":'U',"age":30,"preferences":['A','B','C','D','E','F']},
                 {"name":'V',"age":31,"preferences":['A','C','B','D','E','F']},
                 {"name":'W',"age":40,"preferences":['A','C','B','D','E','F']},
                 {"name":'X',"age":34,"preferences":['A','B','C','D','E','F']},
                 {"name":'Y',"age":45,"preferences":['A','B','C','D','E','F']},
                 {"name":'Z',"age":45,"preferences":['A','B','C','D','F','E']}
                ]

"""

pg = StableRoommates(firstList, secondList)