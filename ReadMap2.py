import osmium as osm
import pandas as pd

fout = open("GentTestSites.txt", "w")


class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def tag_inventory(self, elem, elem_type):
        if elem_type == "node":
            for tag in elem.tags:
                self.osm_data.append([elem_type,
                                      elem.id,
                                      elem.location,
                                      len(elem.tags),
                                      tag.k,
                                      tag.v])

    def node(self, n):
        self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")

    def relation(self, r):
        self.tag_inventory(r, "relation")


def processing():
    amt = 1350
    for index, item in df_osm['type'].items():
        nodes[index] = [item]

    for index, item in df_osm['id'].items():
        nodes[index].append(item)

    for index, item in df_osm['location'].items():
        nodes[index].append(item)

    for index, item in df_osm['ntags'].items():
        nodes[index].append(item)

    for index, item in df_osm['tagkey'].items():
        nodes[index].append(item)
        # TagKeys.append(item)

    for index, item in df_osm['tagvalue'].items():
        nodes[index].append(item)
        amt = index + 1

    return amt


print("Reading...")
osmHandler = OSMHandler()
osmHandler.apply_file("Gent.osm")

data_colnames = ['type', 'id', 'location', 'ntags', 'tagkey', 'tagvalue']
df_osm = pd.DataFrame(osmHandler.osm_data, columns=data_colnames)
# df_osm.tag_genome.sort_values(by=['type', 'id', 'ts'])

print('Processing...')
nodes = {}
nodesTags = {}
nodesID = []
# TagKeys = []
# notHouse = ['route_ref', 'training', 'subject:wikidata', 'railway:ref', 'highway', 'name', 'public_transport',
#             'website', 'brand', 'flag:colour', 'alt_name', 'short_name', 'subject', 'crossing', 'power', 'phone',
#             'barrier', 'office', 'flag:name', 'direction', 'bus', 'operator', 'brand:wikidata', 'amenity', 'source',
#             'train', 'flag:type', 'shop', 'craft', 'noexit', 'trade', 'cycleway', 'official_name', 'traffic_signals',
#             'network', 'railway:position', 'man_made', 'light_rail', 'emergency', 'brand:wikipedia',
#             'operator:wikidata', 'opening_hours', 'railway', 'natural', 'network:type', 'entrance', 'gate']
supermarketIndex = []

amtOfNodes = processing()

print("Sorting...")

for i in range(amtOfNodes):
    id = nodes[i][1]
    if id in nodesTags:
        nodesTags[id].append([nodes[i][-2], nodes[i][-1], nodes[i][2]])
    else:
        nodesTags[id] = [[nodes[i][-2], nodes[i][-1], nodes[i][2]]]
        nodesID.append(id)

for id in nodesID:
    supermarket = False
    # addr = False
    for tag in nodesTags[id]:
        # for word in notHouse:
        #     # print(tag)
        #     if word in tag:
        #         house = False
        # for t in tag:
        #     if 'addr' in t:
        #         addr = True
        if 'supermarket' in tag:
            supermarket = True
    if supermarket:
        supermarketIndex.append(nodesTags[id][0][2])

# for tag in nodesTags[65565265]:
#     for word in notHouse:
#         if word in tag:
#             print(word)

fout.write(str(len(supermarketIndex)) + '\n')
for i in supermarketIndex:
    ans = str(i.lat) + ' ' + str(i.lon) + '\n'
    fout.write(ans)

fout.close()
