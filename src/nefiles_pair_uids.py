#!/usr/bin/python3
#
# Finds unique user IDs in RSICC pickle file, pairs them with /etc/passwd
#
# 20181117 Ondrej Chvala, ochvala@utk.edu

import pickle

data_fname:str = "RSICC.pickle"     # Input file name
fin=open(data_fname,'rb')
myrecs = pickle.load(fin)           # Load RSICC records
#myhashs= pickle.load(fin)

uids  = []                          # UIDs associated with names

for rec in myrecs:
    (uid, name)  = (rec[1], rec[3])
    if (uid, name) not in uids:     # Find unique
        uids.append((uid, name))

uids.sort()                         # For good measure

for rec in uids:                    # Print results
    print(rec)
