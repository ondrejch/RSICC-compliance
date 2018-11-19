#!/usr/bin/python3
#
# Finds unique software IDs in RSICC pickle file
#
# 20181119 Ondrej Chvala, ochvala@utk.edu

import pickle

inst_loc:str = 'UNIVERSITY OF TENNESSEE - KNOXVILLE'

data_fname:str = "RSICC.pickle"     # Input file name
fin = open(data_fname,'rb')
myrecs = pickle.load(fin)           # Load RSICC records
#myhashs= pickle.load(fin)

swids  = {}                         # UIDs associated with names
for r in myrecs:
    if not inst_loc in r[4]:        # Skip SW not installed at our location
        continue

    (swid, swname)  = (r[5], r[6])
    swids[swid] = swname

#print (list(swids.keys()))
#print (sorted(swids.keys()))

for k in sorted(swids.keys()):                     # Print results
    print("%s::%s" % (k,swids[k]))


