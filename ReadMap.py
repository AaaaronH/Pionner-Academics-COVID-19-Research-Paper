# https://download.bbbike.org/osm/bbbike/
# https://www.openstreetmap.org/#map=12/37.3350/-121.8487
fin = open("Gent.osm", "r")
fout = open("GentLatLon.txt", "w")
banWords = ["amenity", "highway"]
pos = []
numOfLines = 139652


def isHouse():
    txtstr = ""
    line = fin.readline()
    while "</node>" not in line:
        txtstr += line
        line = fin.readline()
    for word in banWords:
        if word in txtstr:
            return False
    return True


for i in range(numOfLines):
    line = fin.readline()
    if (line[:6] == "	<node") and "/" not in line:
        if isHouse():
            latPos = line.find("lat=")
            lonPos = line.find("lon=")
            verPos = line.find("version=")
            lat = line[latPos + 5: lonPos - 2]
            lon = line[lonPos + 5: verPos - 2]
            pos.append((lat, lon))

fout.write(str(len(pos)) + "\n")
for i in pos:
    fout.write(i[0] + ' ' + i[1] + "\n")
fout.close()
