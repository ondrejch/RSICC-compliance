#!/usr/bin/python3
#
# Finds unique user IDs in RSICC pickle file, pairs them with /etc/passwd
#
# 20181117 Ondrej Chvala, ochvala@utk.edu

import pickle
import re

inst_loc:str = 'UNIVERSITY OF TENNESSEE - KNOXVILLE'
inst_country:str = 'UNITED STATES'
loc_only:str = 'only valid' 

fin = open('RSICC.pickle','rb')        # RSICC parsed data
myrecs = pickle.load(fin)           # Load RSICC records
#myhashs= pickle.load(fin)
fin.close()

# Associate NEfile groups with RSICC SWIds
swids  = {}                         # SWIds associated with SW names
swgroup= []                         # SWIds associated with nefile group names, note no 1:1 correspondence
negrouplist = []                    # List of nefiles groups corresponding to RSICC data
with open('desc.groups.txt') as fin:# List of SW associated with groups on nefiles
    for line in fin:
        (swid, gname, swname) = line.split(":")
        swid = str(swid)
        if gname:                   # Skip SW that does not exist on nefiles
            swids[swid]   = str(swname)
            swgroup.append( (swid, str(gname), str(swname)) )
            if not gname in negrouplist:   # Make a list of known nefiles groups
                negrouplist.append(gname)
            #print(swid, swgroup)

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
        if gname in negrouplist:
            negroups[gname] = ulist.rstrip().split(",")
            #print(gname, negroups[gname])


def Is_RSICC_group_NIS(swid:str, gname:str) -> bool:
    'Checks if RSICC group corresponds to NIS nefiles group'
    matching = [s for s in swgroup if gname in s]
    if any(swid in s for s in matching):
        #print(" --g> ",swid, gname)
        return True
    return False

def Check_User_Approved(uid:str, gname:str) -> bool:
    'Check is user with RSICC ID uid has access to group gname'
    for r in myrecs:
        #if r[1] == uid and Is_RSICC_group_NIS(r[5], gname):
        if r[1] == uid and Is_RSICC_group_NIS(r[5], gname) and (inst_loc in r[4] or (inst_country in r[4] and not loc_only in r[4])):
            return True
    return False


def Report_Line(uid:str, gname:str) -> str:
    'Write the report line for each user and software'
    rep = ''
    # Full Name; RSICC Customer Number;	Installation where software was received: Request Number: Software Package Name: Software Package ID
    for r in myrecs:
        if r[1] == uid and Is_RSICC_group_NIS(r[5], gname) and (inst_loc in r[4] or (inst_country in r[4] and not loc_only in r[4])):
            rep_line = "".join((r[3],";",r[1],";",r[4],";",r[2],";",r[6],";",r[5],"\n"))
            if not rep_line in rep:
                rep += rep_line
            #print(r[1],r[2],r[3],r[5],r[6]) 
    return rep

# Check if users have permission, write report
report = ""
No_RSICC_history = []
for gname in negroups.keys():
    print("G: ", gname)
    for u in negroups[gname]:
        #print(u, gname)
        if RSICC_UId(u) is None:    # User is not listed at all
            if not u in No_RSICC_history:
                No_RSICC_history.append(u)
        else:
            if Check_User_Approved(RSICC_UId(u), gname):
                #print ("** ", gname, Report_Line(RSICC_UId(u), gname))
                report += Report_Line(RSICC_UId(u), gname)
            else:
                print("ERR! ",  gname, u,  RSICC_UId(u))

# Print report to a file
fout = open("report.csv","w")        # Output text file
print(report, file=fout)
fout.close()

No_RSICC_history.remove('root')
No_RSICC_history.remove('apache')
print("No RSICC history from: ", No_RSICC_history)


