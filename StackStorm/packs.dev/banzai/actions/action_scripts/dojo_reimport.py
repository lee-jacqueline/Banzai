#!/usr/bin/python3

import sys
import os
import re
from defectdojo_api import defectdojo
from st2actions.runners.pythonrunner import Action

# grab DefectDojo container IP
network_file = open("/opt/stackstorm/common/networks.txt", "r")
data = network_file.readlines()
DD_IP = ''
for line in data:
    if re.search('DD_IP', line):
        DD_IP = re.sub('DD_IP=', '', line)
DD_IP = DD_IP.replace('\n', '')
network_file.close()

# grab DefectDojo API Key
apikey_file = open("/opt/stackstorm/common/api_keys.txt", "r")
data = apikey_file.readlines()
api_key = ''
for line in data:
    if re.search('DD_APIKEY', line):
        api_key = re.sub('DD_APIKEY=', '', line)
api_key = api_key.replace('\n', '')
apikey_file.close()

host = "http://" + DD_IP + ":8000"
user = 'admin'

class Dojo_Reimport(Action):
    def run(self, testid, scantype):
        # check params
        print("testid = {}".format(testid))
        print("scan type = {}".format(scantype))
        # instantiate the DefectDojo api wrapper
        dd = defectdojo.DefectDojoAPI(host, api_key, user, debug=True)

        if scantype == 'Nmap Scan':
          filepath = "/opt/stackstorm/scan_results/nmap/nmap_standard.xml"
        elif scantype == 'Burp Scan':
          filepath = "/opt/stackstorm/scan_results/burp/burp_scan.xml"
        elif scantype == 'Nessus Scan':
          filepath = "/opt/stackstorm/scan_results/nessus/nessus_scan.xml"

        # perform upload request + print response
        upload_scan = dd.reupload_scan(testid, scantype, filepath, "true", "2024/1/1", "API")
        print("Test number: {}".format(upload_scan))
