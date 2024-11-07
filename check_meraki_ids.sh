#!/usr/bin/bash

syncdir=`dirname "$(readlink -f "$0")"`
cd $syncdir
#source config

function usage()
{
  echo "This plugin interfaces with Meraki API (v2)"
  echo "Usage: $0 -[hfwc]"
  echo "-h show this message"
  echo "-a meraki api key"
  echo "-o meraki organization id"
  echo "-n meraki network id"
  echo "-f [FUNCTION]"
  echo "        FUNCTION could be any of the following:"
  echo "                ALL = IDS allowed event"
  echo "                BLO = Count blocked event for proactive monitoring"
  echo "-w [WARNING]"
  echo "-c [CRITICAL]"
}

while getopts "h :a: :o: :n: :f: w: c:" opt; do
  case $opt in
    h)
      usage
      exit 0;;
    a)
     API_KEY="$OPTARG"
     export API_KEY
     ;;
    o)
     ORG="$OPTARG"
     export ORG
     ;;
    n)
     NETWORK="$OPTARG"
     export NETWORK
     ;;
    f)
      func="$OPTARG"
      case $func in
        ALL)
           PYCMD=meraki_ids_allowed_event.py
           ;;
        BLO)
           PYCMD='meraki_ids_event_count.py -p message -t 30 -c'
           ;;
        *)
           echo "Invalid function"
           exit 1;;
      esac
      ;;
    w)
      WARN="$OPTARG"
      ;;
    c)
      CRIT="$OPTARG"
      if [[ -z $WARN ]]; then
          WARN=$((CRIT - 1))
      fi
      ;;
    *) usage
      exit 1;;
  esac
done

if [[ $func == BLO ]]; then
        ./$PYCMD $CRIT
else
        ./$PYCMD $WARN $CRIT
fi
