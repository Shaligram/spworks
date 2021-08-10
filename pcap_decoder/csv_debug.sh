#!/bin/bash

base="/nfs-bfs/GCS/Telus_SpeedTest/v6_v8"
yyyymmdd=$(date +%Y%m%d)
WGET="wget --user opwv --password 0p3nw4ve! "
CURL="curl -X POST http://jenkins.bfs.openwave.com:8080/jenkins/job/Pcap_decoder/build --user ojangda:11502d76ca624243d39ae275888a529e00 "
DEBUG=/users/sm0195/pcap_decoder/debug_parser.py
PYTHON=python3
CCTOOL=/users/sm0195/pcap_decoder/ccTool.py

if [ -z "$2" ]
then
echo Suffix not specified in '$1' .
fi

suffix=$2
echo "suffix = (${suffix})"


if [ -z "$1" ]
then
echo 'File or url not specified in $1'
exit 1
elif [ `echo $1 | grep http` ]
then
  filename=$(echo $1 |perl -pi -e's#.*/##g')
  output=$(echo $filename | perl -pi -e"s#.scaInit.log#$suffix#g")  
  basedir="$base/$yyyymmdd/$output"  
  mkdir -p $basedir
  chmod 777 $base/$yyyymmdd
  chmod 777 $basedir
  cd $basedir
  
  if [ "$3" = "0" ]
  then 
    echo "Skipping download"
  else
    rm -f $filename
    echo "Downloading scaInit.log : $WGET $1"
    $WGET $1
  fi
  input="${basedir}/${filename}"
  chmod 777 $input
  echo URL entered : $1 . Downloading to $input basedir $basedir
  cd $basedir
  echo "starting decode"
  $PYTHON $DEBUG --csv --integra -f $input
  echo "starting analysis"
  $PYTHON $CCTOOL -i ./cc_internal.csv -o cc_internal -tpmin 5 -a -perms
fi
