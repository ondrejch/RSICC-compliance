#!/usr/bin/python3
#
# Parses mailbox with RSICC emails and gets out who has access to what
#
# 20181117 Ondrej Chvala, ochvala@utk.edu

import mailbox
import re
from bs4 import BeautifulSoup
import pickle

outdata_fname:str = "RSICC.pickle"          # Output file name
mailbox_fname:str = 'RSICC'                 # Mailbox file name
mbox = mailbox.mbox(mailbox_fname)          # Open mailbox

def get_text(msg) ->str:
    '''Function that parses individual emails in a mailbox and returns plain text'''
    text = ""
    if msg.is_multipart():
        for part in msg.get_payload():
            if part.get_content_type() == 'text/plain':
                text += BeautifulSoup(part.get_payload(decode=True), "html.parser" ).get_text()
            if part.get_content_type() == 'text/html':
                text += BeautifulSoup(part.get_payload(decode=True), "html.parser" ).get_text()
    else:
        text = BeautifulSoup(msg.get_payload(decode=True), "html.parser" ).get_text()
    return text.strip()

# Regexp to remove expected junk that messes up the matching
#reg_remove1 = re.compile(r'\s+This software is only valid for use while associated with this installation(.)?')
reg_remove2 = re.compile(r'^\s+', re.MULTILINE)
reg_remove3 = re.compile(r'\s-\s?$', re.MULTILINE)
# Matching magic, format: [date] [CustomerID] [RequestID] [Name] [Installation] [SoftwareID] [SoftwareName]
reg_match = re.compile(r'''.*Date Requested: ([\d/]+)\s+.*Customer ID: (\d+)\s+.*Request Number: (\d+)\s+.*Name: ([a-zA-Z.\-/ ]*)\s+.*Installation Name: ([a-zA-Z0-9,.\- ]*)\s+.*Software Package ID: ([a-zA-Z0-9 ]*)\s+.*Software Package Name: ([a-zA-Z0-9,.\*\-/ ]*)\s+''')

i:int=0;            # Running index
my_records = []     # List with RSICC data matched by RE above
my_rechash = []     # Hash to check for uniqueness

for msg in mbox:    # Parse the mailbox
    i=i+1
    #print('\n*********************************************************************** ', i)
    print('Processing ', msg['date'], msg['subject'], msg['from'])
    mailbody = get_text(msg)                    # Reads each message
#    mailbody = reg_remove1.sub("",mailbody)     # Removes junk
    mailbody = reg_remove2.sub("",mailbody)
    mailbody = reg_remove3.sub("",mailbody)
    match = reg_match.findall(mailbody)         # Matches RSICC data

    for e in match:                         # For each matched RSICC entry
        if not e in my_records:             # Check if unique
        #if not hash(e) in my_rechash:       # Check if unique - hashing is slower, supposedly python does that
        #     print(e)
          #   my_rechash.append(hash(e))      # Add hash
            my_records.append(e)            # Add entry
        else:
            pass
            #print(e)
#print(mailbody)

print("--> Records found: ", len(my_rechash), len(my_records) )

# Write data pickle
fout = open(outdata_fname,"wb")         # Output pickle file
pickle.dump(my_records,fout)            # Pickle record list
#pickle.dump(my_rechash,fout)            # Pickle hash list
fout.close()

# Print results to a file
fout = open("myrecords.txt","w")        # Output text file
for e in my_records:
     print(e, file=fout)
fout.close()


