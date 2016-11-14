#!/usr/bin/python
import subprocess
import platform
import json
import requests
import pprint

def get_distro_name():
    dist = platform.linux_distribution()
    dist_name = dist[0].replace(' ', '-') + '-' + dist[1].split('.')[0]
    return dist_name

def pprint(jsdict):
    '''
    Pretty printing of JSON structure
    '''
    if not jsdict:
        return
    jsdict_ = jsdict
    if 'json' in dir(jsdict):
        jsdict_ = jsdict.json()
    print json.dumps(jsdict_, sort_keys=True, indent=4, separators=(',', ': '))


dist_name = get_distro_name()
uname = subprocess.check_output('uname -r', shell=True).strip()
api_url = 'https://readykernel.com/api/v1/distros/%(dist_name)s/kernels/%(uname)s/' % vars()
headers = { 
    'Accept': 'application/json',
    'Content-Type': 'application/json', 
}    
response = requests.get(api_url, headers=headers)
kernel = response.json()
# Patches sorted desc by versions - last patch always [0]
last_patch_uri = kernel['patch_set'][0]
response = requests.get(last_patch_uri, headers=headers)
last_patch = response.json()
pprint(last_patch)



