#!/usr/bin/env python3

import requests
import os
import json
import sys, argparse


def timespan_range(timespan):
    if int(timespan) < 0 or int(timespan) > 525600 :
        raise argparse.ArgumentTypeError("Value of timespan can only be between 0 and 525600 minutes")
    return timespan

#Set up the command line arguments
parser = argparse.ArgumentParser(description='Fetches allowed Events from IDS security API with N minutes')
parser.add_argument('-t',metavar='Minutes',default=30,help='Set Time span in Minutes',type=timespan_range)
parser.add_argument('-c',metavar='critical events threshold',default=500,help='if the count of events is > value it will exit with critical signal')
parser.add_argument('-p',metavar='events  type',required=True,help='Group events based on this parameter',choices=['message','srcIp','destIp'])


opts = parser.parse_args()

#30 minutes ago, timespan is in seconds so 30 * 60
timespan=int(opts.t) * 60
# warningThreshold = int(opts.w)
criticalThreshold = int(opts.c)

apiV1 = 'https://api.meraki.com/api/v1/'
url =  apiV1+'networks/' + os.environ['NETWORK'] + '/appliance/security/events?timespan='+str(timespan)
headers = {
    "X-Cisco-Meraki-API-Key": os.environ['API_KEY']
}

response = requests.get(url,headers=headers)
#for troubleshooting
#print response.text
#print response.status_code
#print response.reason
jsonRes = json.loads(response.text)
#Check if the response object contain the parameter used in grouping by
#if( len(jsonRes)> 0 and opts.p not in jsonRes[0]):
#    print("Parameter "+ opts.p+" is not found in event object")
#    print("Key must be one of the following parameters: ")
#    print(''.join(jsonRes[0].keys()))
#    exit(1)

# ##Filter events based on their blocked status
blockedEvents = {}
for event in jsonRes:
    if event.get('blocked')==True:
        key = event.get(opts.p)
        if key is not None:
            blockedEvents[key]=blockedEvents.get(key,0)+1

exitSignal = 0
for key in blockedEvents:
    if(blockedEvents[key] >= criticalThreshold):
            print('Event critical threshold reached detected for '+opts.p +': '+key+': '+str(blockedEvents[key]))
            if(exitSignal!=2):
                exitSignal=2

if(exitSignal==0):
    print('OK:Events are within accepted threshold')

exit(exitSignal)
