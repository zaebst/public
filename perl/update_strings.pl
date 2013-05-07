#!/usr/bin/perl
use strict;

# Updates the Perl ProcessTable Linux.h file when new fields are added to the State enum.
#
# Usage: place in directory with Linux.h file.  Make sure the Linux.h:  static const char strings[] has all fields on a seperate line. 
# It will calculate the offsets for the strings_index[] and field_names[] arrays and print the code to screen.


my $found_struct = 0;
my $total_length = 0;
my $position_before_fields = 0;

my @string_lengths = ();

open(FH, "Linux.h");
while(my $line = <FH>)
{
    if ($found_struct) {
      if ( $line =~ m!.*\"([a-z0\\\/\s]*)\"\s*$! )  { 
        my $new_start = length($1) - 1 ;                   # the \0 counts as 1 char.  So the pointer is at length of string minus 1
        chomp($line);
        #print "Current line ($line).  This string starts at: $total_length\n";
        push(@string_lengths, $total_length);
        if ($line =~ m|.*\"intilization failed\\0\"| ){ $position_before_fields = $total_length } # This string marks the beginning of fields
        $total_length += $new_start;
      }
    }

    if ($line =~ m/static const char strings.*/) { $found_struct = 1; }
    if ($line =~ m/.*I generated this.*/) { $found_struct = 0; }
}
close(FH);

push(@string_lengths, $total_length);

my @strings_prepended = ();
foreach ( @string_lengths ) { if ( $_ > $position_before_fields ) { push(@strings_prepended, $_) } } 
map { $_ = "strings + $_" } @strings_prepended;
pop(@strings_prepended);  # The last value is not a field, it is the default format.

print_c_code("static const size_t strings_index[] =\n{", "};\n", @string_lengths); 
print_c_code("static const char* const field_names[] =\n{", "};\n", @strings_prepended);


sub print_c_code
{
    my $header = shift;
    my $footer = shift;
    my @elements = @_;
    print $header, "\n";
    foreach my $element (@elements) { print "     ", $element, ",\n"; }
    print $footer, "\n";
}

