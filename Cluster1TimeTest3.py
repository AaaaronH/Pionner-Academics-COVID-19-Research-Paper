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
fout = open('Cluster1Time3.txt', 'a')
houses = []
houseNum = int(fin.readline())
for i in range(houseNum):
    houses.append([float(x) for x in fin.readline().split(' ')])


def solve(i, finName, houses, houseNum):

    fin2 = open(finName, 'r')
    print("Reading...")
    testCenters = []
    testNum = int(fin2.readline())
    testNum = i * 5
    for i in range(testNum):
        testCenters.append([float(x) for x in fin2.readline().split(' ')])
    clusters = {}
    clusterID = 0
    clusterType = {}

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

    # print("Solving...")

    fout.write(str(testNum) + ' ' + str(clusterID) + '\n')
    print("Finished.")
    return


if __name__ == '__main__':
    for i in range(1, 16):
        print("------------------------ Berkeley", i * 5, "------------------------")
        # Start foo as a process
        p = multiprocessing.Process(target=solve, name="Solve", args=(i, 'BerkeleyTestSites.txt', houses, houseNum, ))
        p.start()

        # Wait 10 min for foo
        for i in range(20):
            time.sleep(3)
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

    for i in range(1, 21):
        print("------------------------ Gent", i * 5, "------------------------")
        # Start foo as a process
        p = multiprocessing.Process(target=solve, name="Solve", args=(i, 'GentTestSites.txt', houses, houseNum, ))
        p.start()

        for i in range(20):
            time.sleep(3)
            if not p.is_alive():
                break

        if p.is_alive():
            print("TIMEOUT ERROR.")
            p.terminate()

            # Cleanup
            p.join()

    fout.close()

