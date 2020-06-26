#Object Oriented Classes
from Network.StableRoommates import *;
from Network.RandomMates import *;
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

    count = 1    
    print("\nCreating Nodes.")
    for k, value in JsonGeoData.items():
        firstList.append({"name": k, 
                          "id": str(count),
                          "residual": random.choice(ResidualEnergies), 
                          "snr": random.choice(SNRs),
                          "pos": (float(value["geometry"]["location"]['lat']), float(value["geometry"]["location"]['lng']))})
        count += 1

#USERS
FileName = ".\Source\Data\Health Centers\Soweto.json"
with io.open(FileName, 'r', encoding="utf-8") as JsonData:
    JsonGeoData = json.load(JsonData)
    BDs = random.normal(10, 2.1, 100000000)

    count = 1
    print("Creating Users.")
    for k, value in JsonGeoData.items():
        secondList.append({"name": k,
                           "id": str(count),
                           "bandwidwith": random.choice(BDs),
                           "pos": (float(value["geometry"]["location"]['lat']), float(value["geometry"]["location"]['lng']))})
        count += 1

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
    node["preferences"] = preferences

#USERS
Average_Residual = average([(node["residual"]) for node in firstList])
Average_SNR = average([node["snr"] for node in firstList])

for user in secondList:
    preferences = []
    for node in firstList:
        if node["snr"] >= Average_SNR and node["residual"] >= Average_Residual:
            preferences.append(node["name"])
    user["preferences"] = preferences

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

print("Performing Stable Roomate Alloction.")
pg = StableRoommates(firstList, secondList)

USERS = pg.getUsers()

Allocation = {}
Results = {}

PreferredRoommates = 0
PontetialRoommates = 0
CountRandommates = 0

for user in USERS:
    Allocation[str(user.id)] = {"id": user.id,
                                "name": user.name,
                                "pos": user.pos,
                                "preferred": [u for u in user.preferredMates],
                                "stableRoommate": {"id": user.mate.id, 
                                         "name": user.mate.name, 
                                         "pos": user.mate.pos},
                                "randomRoommate": {"id": user.randomMate.id, 
                                         "name": user.randomMate.name, 
                                         "pos": user.randomMate.pos}}
    
    if str(user.mate.name) in [user.name for user in user.potentialMates]:
        PontetialRoommates += 1

    for node in firstList:
        if str(node["name"]) == str(user.name):
            if str(user.mate.name) in node["preferences"]:
                PreferredRoommates += 1
                break;
            else:
                print(user.name, node["preferences"])

    if str(user.randomMate.name) in user.preferredMates:
        CountRandommates += 1

Results = {"totalUsers": len(USERS),
           "pontentialRoommate": PontetialRoommates,
           "preferredRoommate": PreferredRoommates,
           "randomRoommate": CountRandommates}

#Creating an external files
print("\n_______________________________________\nCreating an external files")
with open("./Allocation.json", 'w') as fp: json.dump(Allocation, fp, indent = 4)
fp.close()
with open("./Results.json", 'w') as fp: json.dump(Results, fp, indent = 4)
fp.close()