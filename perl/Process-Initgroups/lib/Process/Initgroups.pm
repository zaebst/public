package Process::Initgroups;

use 5.014002;
use strict;
use warnings;
use Carp;

require Exporter;

our @ISA = qw(Exporter);

# Items to export into callers namespace by default. Note: do not export
# names by default without a very good reason. Use EXPORT_OK instead.
# Do not simply export all your public functions/methods/constants.

# This allows declaration	use Process::Initgroups ':all';
# If you do not need this, moving things directly into @EXPORT or @EXPORT_OK
# will save memory.
our %EXPORT_TAGS = ( 'all' => [ qw(
	
) ] );

our @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );

our @EXPORT = qw(
	
);

our $VERSION = '0.01';

require XSLoader;
XSLoader::load('Process::Initgroups', $VERSION);

# Preloaded methods go here.

# Autoload methods go after =cut, and are processed by the autosplit program.

1;
__END__
# Below is stub documentation for your module. You'd better edit it!

=head1 NAME

Process::Initgroups - Perl extension to use the c function initgroups found on most linux like systems.

=head1 SYNOPSIS

  use Process::Initgroups;
  my $user = 'dave';
  my (undef,undef,$uid,$gid,undef,undef,undef,undef,undef) = getpwnam($user);
  #
  # Here you can use the gid returned by getpwnam, which is the primary group for the user or arbitrarily choose a group with getgrnam
  #  my $gid = getgrnam('some_group_name');
  #
  if( ! Process::Initgroups::initgroups($user,$gid) ) 
  {
       # handle failure 
  }
  # Assuming the goal is to drop privliges, it is still necessary to setgid, then setuid
  if( ! setgid($gid) ) { handle failure }
  if( ! setuid($uid) ) { handle failure }


=head1 DESCRIPTION

Runs initgroups found on most unix/linux systems.  Return codes are the same as POSIX return codes.  Failure: undef.  Success: "0 but true"

=head2 EXPORT

None by default.



=head1 SEE ALSO
Initgroups and setgroups man pages.  
Initgroups will initalize the process with all groups the user belongs to in /etc/groups.

If the user does not require all groups, then use the obscure: $) = "$gid $gid"; which passes the second gid to setgroups();
This will effectively clear the group list and the gid passed will be the only group associated with the process.

Note if the second gid is omitted, then $) = "$gid";  leaves the current process real and effective gid(s) associated with the process.






=head1 AUTHOR

dave, E<lt>dave@E<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2013 by dave;

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.14.2 or,
at your option, any later version of Perl 5 you may have available.


=cut
