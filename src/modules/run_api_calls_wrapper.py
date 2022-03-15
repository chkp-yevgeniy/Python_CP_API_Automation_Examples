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
import helper


def run_api_calls_wrapper(_conf_d, _api_calls_l, _publish):
  title="run_api_calls_wrapper"

  print("### Start "+title+"###") 

  # Get API client object
  client_args = APIClientArgs(server=_conf_d["mgmt_ip"], unsafe_auto_accept=True)
  with APIClient(client_args) as client:           

    api_calls_res_d_l=[]
    api_calls_pure_res_d_l=[]

    # login to server:
    login_res = client.login(_conf_d["mgmt_user"], _conf_d["mgmt_pwd"], domain=_conf_d["domain"])                
    print("--- --- 10. Login on target {} {} {} {}".format(_conf_d["mgmt_user"], _conf_d["domain"], _conf_d["mgmt_ip"], str(login_res.success)))      


    print("--- --- 20. Iterate api calls list")
    for api_call_d in _api_calls_l:
      pprint.pprint(api_call_d)

      print("--- --- 30. Execute api call "+api_call_d["name"])
      body_json=json.dumps(api_call_d["body"])
      api_res_d = client.api_call(api_call_d["name"], body_json)
      pprint.pprint(api_res_d)    
      exit()    
      print("API call result: "+str(api_res_d.success))        
      # Fill api_calls_res_d_l
      helper.fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)
      #pprint.pprint(api_calls_res_d_l)
      api_calls_pure_res_d_l.append(api_res_d)      

    if _publish==True:
      print("--- 40. Execute api call PUBLISH")    
      api_call_d={}
      api_call_d["name"]="publish"      
      api_call_d["body"]={}
      api_res_d = client.api_call(api_call_d["name"], "{}")    
      print("API call result: "+str(api_res_d.success))        
      # Fill api_calls_res_d_l
      helper.fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)
    
    print("--- --- 50. Get statistics")    
    stats_d={}
    stats_d["api_calls_total"]=str(len(api_calls_res_d_l))
    stats_d["api_calls_successful"]=str(len([x for x in api_calls_res_d_l if x["api_call_res"]==True]))
    stats_d["api_calls_failed"]=str(len([x for x in api_calls_res_d_l if x["api_call_res"]==False]))
    print("Statistics")    
    print(json.dumps(stats_d, indent=4, sort_keys=True))

    print("--- --- 70. Summmary")    
    print(json.dumps(api_calls_res_d_l, indent=4, sort_keys=True))
    
  print("### End "+title+"###")  

  return(api_calls_pure_res_d_l)