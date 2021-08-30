import AllTheMethods as atm
from z3 import *

print("Reading...")
# Building Clusters
# fin = open('BerkeleyLatLon.txt', 'r')
# fin2 = open('BerkeleyTestSites.txt', 'r')
fin = open('GentLatLon.txt', 'r')
fin2 = open('GentTestSites.txt', 'r')
houses = []
houseNum = int(fin.readline())
for i in range(houseNum):
    houses.append([float(x) for x in fin.readline().split(' ')])
testCenters = []
testNum = int(fin2.readline())
for i in range(testNum):
    testCenters.append([float(x) for x in fin2.readline().split(' ')])

print("Processing...")
for i in range(1, 21):
    clusters = {}
    clusterID = 0
    clusterType = {}

    minThreshold = i * 1000

    for house in houses:
        centerID = 0
        acceptedCenters = []
        for testCenter in testCenters:
            if atm.dist(house[0], house[1], testCenter[0], testCenter[1]) < minThreshold:
                acceptedCenters.append(centerID)
            centerID += 1
        acceptedCenters = tuple(acceptedCenters)
        if acceptedCenters in clusters:
            clusters[acceptedCenters] += 1
        else:
            clusters[acceptedCenters] = 1
            clusterType[clusterID] = acceptedCenters
            clusterID += 1

    print(i, clusterID)