#!/usr/bin/perl

open(FIL,"docexport.xml") || die;
open(UT,">unescaped.xml") || die;

if(!-e "rst") { mkdir "rst"; }

while($inlin = <FIL>)
{
  $inlin =~ s/\&lt;/</g;
  $inlin =~ s/\&gt;/>/g;
  $inlin =~ s/\x09/ /g;
  $inlin =~ s/ +/ /g;
  $inlin =~ s/ \< / &lt; /g;
  $inlin =~ s/ \<0/ &lt;0/g;
  $inlin =~ s/\> +/>/g;
  $inlin =~ s/ +\</</g;
  $inlin =~ s/^ +//g;
  $inlin =~ s/\/sites\/mhnew.jwp.se\/files\///g;
  $inlin =~ s/\"\/images\//"_images\//g;


  print UT $inlin;
}

close(UT);
close(FIL);

system 'xsltproc stylesheet.xsl unescaped.xml > rst/documentation.rst';
system "sed -i -e 's/^[ ]\\*/\\*/g' rst/documentation.rst";

chdir "rst";

system "rst2pdf documentation.rst";

