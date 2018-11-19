#!/usr/bin/python3
#
# Finds unique user IDs in RSICC pickle file, pairs them with /etc/passwd
#
# 20181117 Ondrej Chvala, ochvala@utk.edu

import pickle
import re

fin = open('RSICC.pickle','rb')     # RSICC parsed data
myrecs = pickle.load(fin)           # Load RSICC records
#myhashs= pickle.load(fin)
fin.close()

uids  = []                          # UIDs associated with names
for rec in myrecs:
    (uid, name)  = (rec[1], rec[3])
    if (uid, name) not in uids:     # Find unique
        uids.append((uid, name))
uids.sort()                         # For good measure

users = []
reg_id = re.compile(r'([\S ]+).*RSICC([\d/]+)')
with open('nefiles_passwd') as fin:# List of NEfiles users
    for line in fin:
        if 'RSICC' in line:
            (login,t,t,t,name,t,t) = line.split(":")
            match = reg_id.findall(name)
#            print(match[0])
            users.append( (match[0][1], login, match[0][0]) )

# Print user full names from both data sources
for u in users:
    for r in uids:
        if u[0] == r[0]:
            print("%30s  %s  %s" % (r[1],u[0],u[2])) 

#for rec in uids:                   # Print results
#    print(rec)
