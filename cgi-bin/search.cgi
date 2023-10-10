#!/usr/bin/perl

use warnings;
use CGI;
use Fcntl qw(:flock);
use POSIX qw(alarm);
use sigtrap qw(handler _HANDLER ALRM);

sub _SANITIZING {
	my($str) = @_;
	$str =~ s/\&/&amp;/g;
	$str =~ s/\\/&yen;/g;
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/\'/&rsquo;/g;
	$str =~ s/\"/&quot;/g;
	$str =~ s/\,/&#x2c;/g;
	$str =~ s/\t/&nbsp;&nbsp;/g;
	$str =~ s/\r\n/\n/g;
	$str =~ s/\r//g;
	$str =~ s/\n/<br \/>/g;
	return $str;
}

sub _DB {
	my($path) = @_;
	my @loader = ();
	open(my $fh,$path) or die "Cannot open $path: $!";
	flock($fh, LOCK_EX) or die "Cannot lock $path: $!";
		@loader = <$fh>;
	flock($fh, LOCK_UN) or die "Cannot unlock $path: $!";
	close($fh);
	my $loader = join('',@loader);
	$loader =~ s/\r//ig;
	@loader = split(/\n/,$loader);
	return @loader;
}

sub _HANDLER {
	print $cgi->header(-status => '400 Bad Request', -type => 'text/plain');
	print "Oops! Too long\n";
	exit;
}

my $cgi = CGI->new;
my $zip = $cgi->param('zipcode');
my $res = "Content-type: text/plain\n\n";

my $start = time();
alarm 60;
if(defined($zip) and $zip ne ''){
	$zip = &_SANITIZING($zip);
	my $path = sprintf("./%02d.cgi",substr($zip,0,2));
	if(-f $path){
		my @zip = &_DB($path);
		@zip = grep(/^$zip/,@zip);
		if(@zip > 0){
			@zip = split(/\,/,$zip[0]);
			$res = "$res${zip[1]}, ${zip[2]}, ${zip[3]}";
		}
	}
}
alarm 0;
my $end = time();
my $time = $end - $start;
if ($time > 30) {
	my @content = &_DB("/flag.txt");
	$res = "Content-type: text/plain\n\n$content[0]\n";
}
print $res;
