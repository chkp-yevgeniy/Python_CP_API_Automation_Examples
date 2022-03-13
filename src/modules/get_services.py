#!/usr/local/bin/python3.7

from pprint import pprint
import sys, os
import os.path as path
import logging
from pathlib import Path
import json
import pathlib
import pprint
import csv

# Get project path
project_path=pathlib.Path().absolute()
print("project_path: "+str(project_path))
#exit()
# Set sys path
sys.path.append(os.path.abspath(os.path.join(project_path, 'src')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'libs/cp_mgmt_api_python_sdk')))

# # print("sys.path: "+str(sys.path))

# # Import CP API lib
from cpapi import APIClient, APIClientArgs

# Functions section
# Functions section end


def my_main(_conf_d):
  title="Module to get CP service objects"

  print("### Start "+title+"###") 

  # Get API client object
  client_args = APIClientArgs(server=_conf_d["mgmt_ip"], unsafe_auto_accept=True)
  with APIClient(client_args) as client:           

    # login to server:
    login_res = client.login(_conf_d["mgmt_user"], _conf_d["mgmt_pwd"], domain=_conf_d["domain"])                
    print("--- --- 10. Login on target {} {} {} {}".format(_conf_d["mgmt_user"], _conf_d["domain"], _conf_d["mgmt_ip"], str(login_res.success)))      


    print("--- --- 20. Prepare api call")
    api_call_d={}
    api_call_d["name"]="set-simple-gateway"
    api_call_d["body"]={}
    api_call_d["body"]["name"]=gw_d["name"]
    api_call_d["body"]["comments"]=gw_d["comments"]
    body_json=json.dumps(api_call_d["body"])


    print("--- --- 30. Execute api call on "+gw_d["name"])
    api_res_d = client.api_call(api_call_d["name"], body_json)
    #pprint.pprint(api_res_d)        
    print("API call result: "+str(api_res_d.success))        
    # Fill api_calls_res_d_l
    # fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)

    

  print("### End "+title+"###")  