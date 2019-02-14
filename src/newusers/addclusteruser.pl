#!/usr/bin/perl -w
# 
# Script to add users to necluster
# Ondrej Chvala
#
use warnings; use strict;

# User input
print "New user netid: ";
my $netid = <STDIN>; chomp $netid;
print "New user name/desc: ";
my $uname = <STDIN>; chomp $uname;

# Check if user exists
my $dogrep = system("grep ^$netid /etc/passwd > /dev/null");
print "User: $netid, $uname \n";
if (not $dogrep) { die "User  $netid exists, quitting"; }

# Make user
my $pwg = `pwgen 15 1`; chomp $pwg;
system("adduser -c \"$uname\" $netid");
system("echo $netid:$pwg | chpasswd");
print "Your necluster login is your NetID, pass: $pwg\nPlease check https://necluster.ne.utk.edu/wiki/\n";

# Setup user
system("runuser -u $netid ./setup_env.sh");

print "All OK!\n";


