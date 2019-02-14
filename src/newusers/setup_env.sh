#/bin/bash

# user setup script
cat /dev/zero | ssh-keygen -q -N '' > /dev/null
ssh-keyscan necluster.ne.utk.edu >> ~/.ssh/known_hosts > /dev/null
cat ~/.ssh/id_rsa.pub >>  ~/.ssh/authorized_keys
ssh necluster.ne.utk.edu hostname

