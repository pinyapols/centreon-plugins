#!/usr/bin/env python3

import requests
import os
import json
import sys, argparse
import datetime

def timespan_range(timespan):
    if int(timespan) < 0 or int(timespan) > 525600 :
        raise argparse.ArgumentTypeError("Value of timespan can only be between 0 and 525600 minutes")
    return timespan

#Set up the command line arguments
parser = argparse.ArgumentParser(description='Fetches allowed Events from IDS security API with N minutes')
parser.add_argument('-t',metavar='Minutes',default=120,help='Set Time span in Minutes',type=timespan_range)
opts = parser.parse_args()

#30 minutes ago, timespan is in seconds so 30 * 60
timespan=int(opts.t) * 60
apiV1 = 'https://' + os.environ['API_HOSTNAME'] + '/api/v1/'
url =  apiV1+'networks/' + os.environ['NETWORK'] + '/appliance/security/events?timespan='+str(timespan)
headers = {
    "X-Cisco-Meraki-API-Key": os.environ['API_KEY']
}

response = requests.get(url,headers=headers)
jsonRes = json.loads(response.text)
# print (jsonRes)
##Filter events based on their blocked status
allowedIDS = [record for record in jsonRes if record.get('blocked') == False]

report=''

if len(allowedIDS) > 0 :
    report+='Critical:IDS allowed event detected'

    for event in allowedIDS :
        report+='\n'+event.get('ts') + ':' + event.get('eventType')+':'+event.get('ruleId')+':'+event.get('message')

    print(report)
    exit(2)

print('OK:No allowed events detected')
exit(0)
