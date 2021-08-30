import AllTheMethods as atm
from z3 import *
import time
import multiprocessing

# print("Reading...")
# Building Clusters
fin = open('BerkeleyLatLon.txt', 'r')
# fin2 = open('BerkeleyTestSites.txt', 'r')
# fin = open('GentLatLon.txt', 'r')
# fin2 = open('GentTestSites.txt', 'r')
fout = open('Cluster2Time3.txt', 'a')
houses = []
houseNum = int(fin.readline())
for i in range(houseNum):
    houses.append([float(x) for x in fin.readline().split(' ')])


def solve(i, finName, houses, houseNum, d):
    startTime = time.time()
    fin2 = open(finName, 'r')
    print("Reading...")
    testCenters = []
    testNum = int(fin2.readline())
    testNum = i
    for i in range(testNum):
        testCenters.append([float(x) for x in fin2.readline().split(' ')])
    readTime = time.time()
    clusters = {}
    clusterID = 0
    clusterType = {}
    minThreshold = d * 3000

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

    processTime = time.time()
    print("Solving...")
    # Solving
    s = Optimize()

    z3_testCenters = [Bool('testingCenter_%i' % i) for i in range(testNum)]
    s.add(Sum([If(z3_testCenters[i], 1, 0) for i in range(testNum)]) <= 10)
    z3_clusters = [Bool('cluster_%s' % i) for i in range(clusterID)]

    for id in range(len(z3_clusters)):
        choices = clusterType[id]
        available = []
        for choice in choices:
            available.append(z3_testCenters[choice])
        if len(available) == 0:
            s.add(z3_clusters[id] == False)
        else:
            s.add(z3_clusters[id] == Or(available))

    h = s.maximize(Sum([If(z3_clusters[i], clusters[clusterType[i]], 0) for i in range(len(z3_clusters))]))
    if s.check() == sat:
        m = s.model()
        result = sorted([(d, m[d]) for d in m], key=lambda x: str(x[0]))[-testNum:]

    solveTime = time.time()
    fout.write(str(testNum) + ' ' + str(minThreshold) + ' ' + str(clusterID) + '\n')
    fout.write(str(h.value().as_long() / houseNum * 100) + '\n')
    output = str(solveTime - startTime) + '\n'
    fout.write(output)
    print("Finished.")
    return


if __name__ == '__main__':

    bList = [10, 20, 30, 40, 50, 60, 70, 79]
    gList = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 106]

    for d in range(1, 3):
        for i in bList:
            print("------------------------ Berkeley", i, d * 3000, "------------------------")
            # Start foo as a process
            p = multiprocessing.Process(target=solve, name="Solve", args=(i, 'BerkeleyTestSites.txt', houses, houseNum, d, ))
            p.start()

            for i in range(6):
                time.sleep(5)
                if not p.is_alive():
                    break

            if p.is_alive():
                # fout.write("FAILED" + '\n')
                print("TIMEOUT ERROR.")
                p.terminate()

                # Cleanup
                p.join()

    fin = open('GentLatLon.txt', 'r')
    houses = []
    houseNum = int(fin.readline())
    for i in range(houseNum):
        houses.append([float(x) for x in fin.readline().split(' ')])

    for d in range(1, 3):
        for i in gList:
            print("------------------------ Gent", i, d * 3000, "------------------------")
            # Start foo as a process
            p = multiprocessing.Process(target=solve, name="Solve", args=(i, 'GentTestSites.txt', houses, houseNum, d, ))
            p.start()

            # Wait 10 seconds for foo
            for i in range(6):
                time.sleep(5)
                if not p.is_alive():
                    break

            if p.is_alive():
                # fout.write("FAILED" + '\n')
                print("TIMEOUT ERROR.")
                p.terminate()

                # Cleanup
                p.join()


    fout.close()

