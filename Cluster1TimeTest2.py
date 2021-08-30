import AllTheMethods as atm
from z3 import *
import time
import multiprocessing

# print("Reading...")
# Building Clusters
fin = open('BerkeleyLatLonSmall.txt', 'r')
# fin2 = open('BerkeleyTestSites.txt', 'r')
# fin = open('GentLatLon.txt', 'r')
# fin2 = open('GentTestSites.txt', 'r')
fout = open('Cluster1Time3.txt', 'a')
houses = []
houseNum = int(fin.readline())
for i in range(houseNum):
    houses.append([float(x) for x in fin.readline().split(' ')])


def solve(i, finName, houses, houseNum):
    startTime = time.time()
    fin2 = open(finName, 'r')
    print("Reading...")
    testCenters = []
    testNum = int(fin2.readline())
    testNum = i * 10
    for i in range(testNum):
        testCenters.append([float(x) for x in fin2.readline().split(' ')])
    clusters = {}
    clusterID = 0
    clusterType = {}
    readTime = time.time()
    print("Processing...")
    for house in houses:
        distances = [atm.dist(house[0], house[1], center[0], center[1]) for center in testCenters]
        centerID = [i for i in range(testNum)]
        result = sorted(zip(distances, centerID))
        key = tuple([key for _, key in result])
        distances = [distance for distance, _ in result]
        if key in clusters:
            clusters[key] = [a + b for a, b in zip(clusters[key], distances)]
        else:
            clusters[key] = distances
            clusterType[clusterID] = key
            clusterID += 1
    processTime = time.time()
    # print(clusterID)
    # print(clusters)

    print("Solving...")
    # Solving
    s = Optimize()

    z3_testCenters = [Bool('testingCenter_%i' % i) for i in range(testNum)]
    s.add(Sum([If(z3_testCenters[i], 1, 0) for i in range(testNum)]) <= 5)
    z3_totalDistance = Real('totalDistance')
    # totalDistance = 0
    z3_clusters = [Real('cluster_%s' % i) for i in range(clusterID)]

    for id in range(len(z3_clusters)):
        choices = clusterType[id]
        clause = False
        for i in reversed(choices):
            clause = If(z3_testCenters[i], z3_clusters[id] == clusters[choices][choices.index(i)], clause)
        # print(clusters[choices], choices, clusters[choices][choices.index(9)])
        s.add(clause)
    # for cluster in z3_clusters:
    #     print(cluster)

    # s.add(z3_totalDistance == Sum(z3_clusters))
    h = s.minimize(Sum(z3_clusters))

    if s.check() == sat:
        m = s.model()
        result = sorted([(d, m[d]) for d in m], key=lambda x: str(x[0]))[-testNum - 1:]

    # for i in result:
    #     print(i)
    solveTime = time.time()
    fout.write(str(testNum) + ' ' + str(clusterID) + '\n')
    fout.write(str(h.value().numerator().as_long() / h.value().denominator().as_long() / houseNum) + '\n')
    output = str(readTime - startTime) + ' ' + str(processTime - readTime) + ' ' + str(solveTime - processTime) + '\n'
    fout.write(output)
    print("Finished.")
    return


if __name__ == '__main__':
    for i in range(1, 8):
        print("------------------------ Berkeley", i * 10, "------------------------")
        # Start foo as a process
        p = multiprocessing.Process(target=solve, name="Solve", args=(i, 'BerkeleyTestSites.txt', houses, houseNum, ))
        p.start()

        # Wait 10 min for foo
        for i in range(600):
            time.sleep(1)
            if not p.is_alive():
                break

        if p.is_alive():
            print("TIMEOUT ERROR.")
            p.terminate()

            # Cleanup
            p.join()

    fin = open('GentLatLon.txt', 'r')
    houses = []
    houseNum = int(fin.readline())
    for i in range(houseNum):
        houses.append([float(x) for x in fin.readline().split(' ')])

    for i in range(1, 11):
        print("------------------------ Gent", i * 10, "------------------------")
        # Start foo as a process
        p = multiprocessing.Process(target=solve, name="Solve", args=(i, 'GentTestSites.txt', houses, houseNum, ))
        p.start()

        for i in range(600):
            time.sleep(1)
            if not p.is_alive():
                break

        if p.is_alive():
            print("TIMEOUT ERROR.")
            p.terminate()

            # Cleanup
            p.join()

    fout.close()

