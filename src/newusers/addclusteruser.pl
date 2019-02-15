#!/usr/bin/perl -w
# 
# Script to add users to necluster
# Ondrej Chvala
#
use warnings; use strict;

# User input
print "New user netid: ";
my $netid = <STDIN>; chomp $netid;

# Check if user exists
my $dogrep = system("grep ^$netid /etc/passwd > /dev/null");
if (not $dogrep) { die "User  $netid exists, quitting"; }

# User description
print "New user name/desc: ";
my $uname = <STDIN>; chomp $uname;

# Make user
print "Making user: $netid, $uname \n";
my $pwg = `pwgen 15 1`; chomp $pwg;
system("adduser -c \"$uname\" $netid");
system("echo $netid:$pwg | chpasswd");
system("make -C /var/yp");

print "\nYour necluster login is your NetID, pass: $pwg\nPlease check https://necluster.ne.utk.edu/wiki/\n\n";

# Setup user
system("runuser -u $netid ./setup_env.sh");

print "All OK!\n";


