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

# Functions section
# Functions section end


def my_main(_conf_d):
  title="Module to add CP service objects"


  print("### Start "+title+"###") 

  _conf_d["service_report_file_json"]=os.path.join(_conf_d["reports_folder"], "services.json")
  _conf_d["service_report_file_csv"]=os.path.join(_conf_d["reports_folder"], "services.csv")
   
  serv_d_l=[]
  api_calls_res_d_l=[]


  print("--- --- 5. Read file with tcp services to be configured")   
  services_l=helper.read_yaml_file(_conf_d["policy_packages_yml"])
  print("Policy packages to be configured: ")
  pprint.pprint(services_l)
  

  # Get API client object
  client_args = APIClientArgs(server=_conf_d["mgmt_ip"], unsafe_auto_accept=True)
  with APIClient(client_args) as client:           

    # login to server:
    login_res = client.login(_conf_d["mgmt_user"], _conf_d["mgmt_pwd"], domain=_conf_d["domain"])                
    print("--- --- 10. Login on target {} {} {} {}".format(_conf_d["mgmt_user"], _conf_d["domain"], _conf_d["mgmt_ip"], str(login_res.success)))      


    print("--- --- 20. Iterate over tcp_services list")
    for package_d in services_l:

      print("--- --- 30. Prepare api call")
      api_call_d={}
      api_call_d["name"]="add-package"      
      api_call_d["body"]={}
      api_call_d["body"]["name"]=package_d["name"]
      api_call_d["body"]["access"]=package_d["access"]
      api_call_d["body"]["comments"]=package_d["comments"]
      body_json=json.dumps(api_call_d["body"])


      print("--- --- 30. Execute api call "+api_call_d["name"])
      api_res_d = client.api_call(api_call_d["name"], body_json)
      #pprint.pprint(api_res_d)        
      print("API call result: "+str(api_res_d.success))        
      # Fill api_calls_res_d_l
      helper.fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)
      #pprint.pprint(api_calls_res_d_l)      

    print("--- 40. Execute api call PUBLISH")    
    api_call_d={}
    api_call_d["name"]="publish"      
    api_call_d["body"]={}
    api_res_d = client.api_call(api_call_d["name"], "{}")    
    print("API call result: "+str(api_res_d.success))        
    # Fill api_calls_res_d_l
    helper.fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)

    
    print("--- --- 40. Get statistics")    
    stats_d={}
    stats_d["api_calls_total"]=str(len(api_calls_res_d_l))
    stats_d["api_calls_successful"]=str(len([x for x in api_calls_res_d_l if x["api_call_res"]==True]))
    stats_d["api_calls_failed"]=str(len([x for x in api_calls_res_d_l if x["api_call_res"]==False]))
    print("Statistics")
    #pprint.pprint(stats_d)
    print(json.dumps(stats_d, indent=4, sort_keys=True))


    # print("--- --- 50. Write result into json")    
    # with open(_conf_d["service_report_file_json"], 'w') as f:
    #   json.dump(serv_d_d, f, sort_keys = True, indent = 4, ensure_ascii = False)    
    

    # print("--- --- 60. Write result into csv")    
    # helper.write_list_of_dicst_into_csv(serv_d_l, _conf_d["service_report_file_csv"])  
    

    print("--- --- 70. Summmary")    
    print(json.dumps(api_calls_res_d_l, indent=4, sort_keys=True))
    
  print("### End "+title+"###")  