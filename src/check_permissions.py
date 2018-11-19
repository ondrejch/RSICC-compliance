#!/usr/bin/python3
#
# Finds unique user IDs in RSICC pickle file, pairs them with /etc/passwd
#
# 20181117 Ondrej Chvala, ochvala@utk.edu

import pickle
import re

inst_loc:str = 'UNIVERSITY OF TENNESSEE - KNOXVILLE'

fin = open('RSICC.pickle','rb')        # RSICC parsed data
myrecs = pickle.load(fin)           # Load RSICC records
#myhashs= pickle.load(fin)
fin.close()

# Associate NEfile groups with RSICC SWIds
swids  = {}                         # SWIds associated with SW names
swgroup= {}                         # SWIds associated with nefile group names
with open('desc.groups.txt') as fin:# List of SW associated with groups on nefiles
    for line in fin:
        (swid, gname, swname) = line.split(":")
        if gname:                   # Skip SW that does not exist on nefiles
            swids[swid]   = swname
            swgroup[swid] = gname
            #print(swid, swgroup[swid])

# Load NEfiles users
users = []
reg_id = re.compile(r'([\S ]+).*RSICC([\d/]+)')
with open('nefiles_passwd') as fin:# List of NEfiles users
    for line in fin:
        if 'RSICC' in line:
            (login,t,t,t,name,t,t) = line.split(":")
            match = reg_id.findall(name)
            users.append( (match[0][1], login, match[0][0]) ) # rsiccID, nefiles login, nefiles description

def RSICC_UId(uname:str) ->str:
    'Returns RSICC userID based on login name'
    for u in users:
        if uname == u[1]:
            return u[0]
    return None

# Load NEfiles user groups
negroups = {}
with open('nefiles_group') as fin:# List of NEfiles groups
    for line in fin:
        (gname,t,t,ulist) = line.split(":")
        if gname in swgroup.values():
            negroups[gname] = ulist.rstrip().split(",")
            #print(gname, negroups[gname])


def Is_RSICC_group_NIS(swid:str, gname:str) -> bool:
    'Checks if RSICC group corresponds to NIS nefiles group'
    for swid in swgroup.keys():
        if swgroup[swid] == gname:
            return True
    return False


def Check_User_Approved(uid:str, gname:str) -> bool:
    'Check is user with RSICC ID uid has access to group gname'
    for r in myrecs:
        if r[1] == uid and Is_RSICC_group_NIS(r[5], gname):
            return True
    return False

# Check if users have permission
No_RSICC_history = []
for gname in negroups.keys():
    for u in negroups[gname]:
        if RSICC_UId(u) is None:    # User is not listed at all
            if not u in No_RSICC_history:
                No_RSICC_history.append(u)
        else:
            if Check_User_Approved(RSICC_UId(u), gname):
                print("OOK! ",  gname, u,  RSICC_UId(u))
            else:
                print("ERR! ",  gname, u,  RSICC_UId(u))
No_RSICC_history.remove('root')
No_RSICC_history.remove('apache')
print("No RSICC history from: ", No_RSICC_history)
for u in No_RSICC_history:
    print("%s@vols.utk.edu" % u)


