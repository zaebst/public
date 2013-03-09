# Before `make install' is performed this script should be runnable with
# `make test'. After `make install' it should work as `perl Process-Initgroups.t'

#########################

# change 'tests => 1' to 'tests => last_test_to_print';

use strict;
use warnings;

use Test::More tests => 1;
BEGIN { use_ok('Process::Initgroups') };

# This is really hard to test because we need to supply a valid user id on the system to test
# To Do: Add real tests
#
#my $ret = Process::Initgroups::initgroups("dave", 10000001);
#$) = 1000;
#$( = 1000;
#$) = 0;
#$( = 0;
#print $),"\n";
#print $(,"\n";
#if ( defined ( $ret ) ) { print $ret, "\n"; }
#else { print "undef\n"; }

#########################

# Insert your test code below, the Test::More module is use()ed here so read
# its man page ( perldoc Test::More ) for help writing this test script.

