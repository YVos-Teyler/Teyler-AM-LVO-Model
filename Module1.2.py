import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

df_met_buurschade = pd.read_excel('excel_buurschade - Copy.xlsx')


#create an empty directed graph
G = nx.DiGraph()
df_met_buurschade['matches'] = df_met_buurschade['matches'].astype('object')

#start progress bar
length_dataset = len(df_met_buurschade)
pbar = tqdm(desc= 'build graph', total = length_dataset )
#iterate through the list
for index, row in df_met_buurschade.iterrows():
    
    pbar.update(1)
    uuid = row['uuid']
    print(uuid)
    # add the uuid as node
    G.add_node(uuid)
    #iterate through related uuids
    for related_uuid in row['matches']:
        #add the related uuid as node
        print(related_uuid)
        G.add_node(related_uuid)
        #add an edge between the uuid and related uuid
        G.add_edge(uuid,related_uuid)

uuid1 = '{760da390-6367-4a19-8a2c-4692421ac3fa}'
#get all related uuids for a given uuid
related_uuids = list(nx.descendants(G,uuid1))
print(related_uuids)

# print('starting draw')
# nx.draw(G, with_labels=True)
# plt.show()

#print(related_uuids)