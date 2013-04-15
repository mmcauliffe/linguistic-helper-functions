#!/usr/bin/perl -w

use WordNet::QueryData;
use WordNet::Similarity::lesk;

$wn = new WordNet::QueryData;
$leskObj = new WordNet::Similarity::lesk($wn);

$one = $ARGV[0];
@twos = split(/,/,$ARGV[1]);

my @values = ();

#print '@twos';

foreach my $item (@twos) {
	$value = process($one, $item);
	#print "$value\n";
	if ($value != -1){
	push(@values,$value);
	}
}

$spstring = join(',',@values);

print STDOUT "$spstring";

#Begin slightly modified Similarity code
sub process
{
  my $input1 = shift;
  my $input2 = shift;
  my $word1 = $input1;
  my $word2 = $input2;
  my $wps;
  my @w1options;
  my @w2options;
  my @senses1;
  my @senses2;
  my %distanceHash;

  if(!(defined $word1 && defined $word2))
  {
    print STDERR "Undefined input word(s).\n";
    return (-1);
  }
  $word1 =~ s/[\r\f\n]//g;
  $word1 =~ s/^\s+//;
  $word1 =~ s/\s+$//;
  $word1 =~ s/\s+/_/g;
  $word2 =~ s/[\r\f\n]//g;
  $word2 =~ s/^\s+//;
  $word2 =~ s/\s+$//;
  $word2 =~ s/\s+/_/g;
  @w1options = &getWNSynsets($word1);
  @w2options = &getWNSynsets($word2);

  if(!(scalar(@w1options) && scalar(@w2options)))
  {
    #print STDERR "'$word1' not found in WordNet.\n" if(!scalar(@w1options));
    #print STDERR "'$word2' not found in WordNet.\n" if(!scalar(@w2options));
    return (-1);
  }

  @senses1 = ();
  @senses2 = ();
  foreach $wps (@w1options)
  {
    if($wps =~ /\#([nvar])\#/)
    {
      push(@senses1, $wps);
    }
  }
  foreach $wps (@w2options)
  {
    if($wps =~ /\#([nvar])\#/)
    {
      push(@senses2, $wps);
    }
  }
	
  if(!scalar(@senses1) || !scalar(@senses2))
  {
    print STDERR "Possible part(s) of speech of word(s) cannot be handled by module.\n";
    return (-1);
  }

  %distanceHash = &getDistances([@senses1], [@senses2]);

  
    my ($key) = sort {$distanceHash{$b} <=> $distanceHash{$a}} keys %distanceHash;
    return ($distanceHash{$key});
}

# Subroutine to get all possible synsets corresponding to a word(#pos(#sense))
sub getWNSynsets
{
  my $word = shift;
  my $pos;
  my $sense;
  my $key;
  my @senses;
  return () if(!defined $word);

  # First separately handle the case when the word is in word#pos or
  # word#pos#sense form.
  if($word =~ /\#/)
  {
    if($word =~ /^([^\#]+)\#([^\#])\#([^\#]+)$/)
    {
      $word = $1;
      $pos = $2;
      $sense = $3;
      return () if($sense !~ /[0-9]+/ || $pos !~ /^[nvar]$/);
      @senses = $wn->querySense($word."\#".$pos);
      foreach $key (@senses)
      {
        if($key =~ /\#$sense$/)
        {
          return ($key);
        }
      }
      return ();
    }
    elsif($word =~ /^([^\#]+)\#([^\#]+)$/)
    {
      $word = $1;
      $pos = $2;
      return () if($pos !~ /[nvar]/);
    }
    else
    {
      return ();
    }
  }
  else
  {
    $pos = "nvar";
  }

  # Get the senses corresponding to the raw form of the word.
  @senses = ();
  foreach $key ("n", "v", "a", "r")
  {
    if($pos =~ /$key/)
    {
      push(@senses, $wn->querySense($word."\#".$key));
    }
  }

  # If no senses corresponding to the raw form of the word,
  # ONLY then look for morphological variations.
  if(!scalar(@senses))
  {
    foreach $key ("n", "v", "a", "r")
    {
      if($pos =~ /$key/)
      {
        my @tArr = ();
        push(@tArr, $wn->validForms($word."\#".$key));
        push(@senses, $wn->querySense($tArr[0])) if(defined $tArr[0]);
      }
    }
  }
  return @senses;
}

# Subroutine to compute relatedness between all pairs of senses.
sub getDistances
{
  my $list1 = shift;
  my $list2 = shift;
  my $synset1;
  my $synset2;
  my $tracePrinted = 0;
  my %retHash = ();
  return {} if(!defined $list1 || !defined $list2);
  my %errcache;
LEVEL2:

  foreach $synset1 (@{$list1})
  {
    foreach $synset2 (@{$list2})
    {

      # modified 12/8/03 by JM
      # it is possible for getRelatedness to return a non-numeric value,
      # and this can cause problems in ::process() when the relatedness
      # values are sorted
      #$retHash{"$synset1 $synset2"} = $leskObj->getRelatedness($synset1, $synset2);
      my $score = $leskObj->getRelatedness($synset1, $synset2);
      $retHash{"$synset1 $synset2"} = $score;
      my ($err, $errString) = $leskObj->getError();

      #end modifications
      if($err)
      {

        # 12/9/03 JM (#1)
        # cache error strings indicating that two words belong
        # to different parts of speech
        $errString =~ m/(\S+\#[nvar])(?:\#\d+)? and (\S+\#[nvar])(?:\#\d+)?/;
        my $keystr = "$1 $2";
        print STDERR "$errString\n" unless $errcache{$keystr};
        $errcache{$keystr} = 1;

        # JM 12/8/2003
        # getRelatedness() can return a warning if the two concepts
        # are from different taxonomies, but we need to keep
        # comparing relatedness values anyways
        #
        # last LEVEL2;
        last LEVEL2 if ($err > 1);
      }
      if(defined $opt_trace)
      {
        my $loctr = $leskObj->getTraceString();
        if($loctr !~ /^\s*$/)
        {
          print "$synset1 $synset2:\n";
          print "$loctr\n";
          $tracePrinted = 1;
        }
      }
    }
  }
  print "\n\n" if(defined $opt_trace && $tracePrinted);
  return %retHash;
}


exit;
