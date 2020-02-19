

'''
different ways to get the tube infomation from TFL
first section gets either a station or second produces all stations
'''

import requests
import sys

def station():

    xx = ['Bakerloo','Victoria','Jubilee']
    for i in xx:
        url = 'https://api.tfl.gov.uk/Line/{0}/Status?'.format(i)

        a = requests.get(url)
        dataq = a.json()
        #for i in dataq:
            #print(i['lineStatuses'][0]['statusSeverityDescription'])
        for i in dataq:
            print("{}".format(i['name']))
            for status in i['lineStatuses']:
                print("   {}".format(status['statusSeverityDescription']))
                if status['statusSeverity'] != 10:
                    print("        {}".format(status['reason']))
#station()


def multistation():
    url = ('https://api.tfl.gov.uk/line/mode/tube,overground/status')
    b = requests.get(url)
    all_lines_status = {}

    dataq = b.json()
    for i in dataq:
        print("{}".format(i['name']))
        for status in i['lineStatuses']:
            print("   {}".format(status['statusSeverityDescription']))
            if status['statusSeverity'] != 10:
                print("        {}".format(status['reason']))
        #print('\n')

#multistation()





'''
this is simular but playing around with saving data in dictonary format and pulling out that data.
orginal code found at:
https://github.com/raulbarrue/tfl_raspberrypi
'''
import json
import requests


#################
def get_status():
    url = ('https://api.tfl.gov.uk/line/mode/tube,overground/status')
    b = requests.get(url)
    js = b.json()
    all_lines_status = {}

    for i in range(0, len(js)):
        #print(js)
        status_code = js[i]["lineStatuses"][0]["statusSeverity"]
        line_name = js[i]["name"]
        all_lines_status[line_name] = status_code

    print(all_lines_status)
    return all_lines_status

    #
    # for i in range(0, len(js)):
    #     #print(js)
    #     status_code = js[i]["lineStatuses"][0]["statusSeverity"]
    #     #print(status_code)
    #     #if status_code != 10:
    #     #    reason = js[i]["lineStatuses"][0]["reason"]
    #     #reason = js[i]["lineStatuses"][0]["reason"]
    #     line_name = js[i]["name"]
    #     all_lines_status[line_name] = [status_code]
    #     #all_lines_status[line_name] = reason
    #     #break
    # print(all_lines_status)
    # return all_lines_status


def output():
    all_lines = get_status()  # Get the status of all lines
    print(all_lines)

    for line in all_lines:
        reason = all_lines[line][0]
        if all_lines[line][0] == 10:
            print(line + ": Good Service")
        elif all_lines[line][0] == 6:
            print(line + ": Severe Delays")
        elif all_lines[line][0] == 9:
            print(line + ": Minor Delays")
        elif all_lines[line][0] == 5:
            print(line + ": Part Closure")
            if reason != 10:
                print(all_lines[line][1])
        elif all_lines[line][0] == 20:
            print(line + ": Service Closed")
            #if reason != 10:
             #   print(all_lines[line][1])
        elif all_lines[line][0] == 3:
            print(line + ": Part Suspended")
        else:
            print(line + ": Unknown Status")

get_status()
#output()