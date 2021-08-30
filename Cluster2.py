import AllTheMethods as atm
from z3 import *

print("Reading...")
# Building Clusters
fin = open('BerkeleyLatLon.txt', 'r')
fin2 = open('BerkeleyTestSites.txt', 'r')
# fin = open('GentLatLon.txt', 'r')
# fin2 = open('GentTestSites.txt', 'r')
houses = []
houseNum = int(fin.readline())
for i in range(houseNum):
    houses.append([float(x) for x in fin.readline().split(' ')])
testCenters = []
testNum = int(fin2.readline())
for i in range(testNum):
    testCenters.append([float(x) for x in fin2.readline().split(' ')])

clusters = {}
clusterID = 0
clusterType = {}
minThreshold = 7000

print("Processing...")
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

print(clusterID)
# print(clusters)
print("Solving...")
# Solving
s = Optimize()

z3_testCenters = [Bool('testingCenter_%i' % i) for i in range(testNum)]
s.add(Sum([If(z3_testCenters[i], 1, 0) for i in range(testNum)]) <= 10)
z3_clusters = [Bool('cluster_%s' % i) for i in range(clusterID)]
accepted = Bool('accepted')
amtOfPeople = 0
z3_amtOfPeople = Int('amtOfPeople')

for id in range(len(z3_clusters)):
    choices = clusterType[id]
    available = []
    for choice in choices:
        available.append(z3_testCenters[choice])
    if len(available) == 0:
        s.add(z3_clusters[id] == False)
    else:
        s.add(z3_clusters[id] == Or(available))

# s.add(And(z3_clusters) == True)

h = s.maximize(Sum([If(z3_clusters[i], clusters[clusterType[i]], 0) for i in range(len(z3_clusters))]))
if s.check() == sat:
    m = s.model()
    result = sorted([(d, m[d]) for d in m], key=lambda x: str(x[0]))[-testNum:]

for i in result:
    print(i)

print(h.value().as_long() / houseNum * 100)
