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
#print("project_path: "+str(project_path))
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
  title="Module to get CP service objects"

  print("### Start "+title+"###") 
  #exit()

  _conf_d["service_report_file_json"]=os.path.join(_conf_d["reports_folder"], "services.json")
  _conf_d["service_report_file_csv"]=os.path.join(_conf_d["reports_folder"], "services.csv")
   
  serv_d_l=[]

  # Get API client object
  client_args = APIClientArgs(server=_conf_d["mgmt_ip"], unsafe_auto_accept=True)
  with APIClient(client_args) as client:           

    # login to server:
    login_res = client.login(_conf_d["mgmt_user"], _conf_d["mgmt_pwd"], domain=_conf_d["domain"])                
    print("--- --- 10. Login on target {} {} {} {}".format(_conf_d["mgmt_user"], _conf_d["domain"], _conf_d["mgmt_ip"], str(login_res.success)))      


    print("--- --- 20. Prepare api call")
    api_call_d={}
    api_call_d["name"]="show-packages"
    api_call_d["body"]={}
    api_call_d["body"]["limit"]="50"    
    api_call_d["body"]["offset"]="0"
    #api_call_d["body"]["details-level"]="full"
    body_json=json.dumps(api_call_d["body"])


    print("--- --- 30. Execute api call "+api_call_d["name"])
    api_res_d = client.api_call(api_call_d["name"], body_json)
    pprint.pprint(api_res_d)        
    exit()
    print("API call result: "+str(api_res_d.success))        
    # Fill api_calls_res_d_l
    # fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)

    for api_res_serv_tcp_d in api_res_d.data["objects"]:
      serv_tcp_d={}
      serv_tcp_d["name"]=api_res_serv_tcp_d["name"]
      serv_tcp_d["port"]=api_res_serv_tcp_d["port"]
      serv_tcp_d["type"]=api_res_serv_tcp_d["type"]
      serv_d_l.append(serv_tcp_d)   


    print("--- --- 40. Transform to dict and get statistics")    
    serv_d_d={}
    serv_d_d["objects"]=serv_d_l
    serv_d_d["total"]=str(len(serv_d_l))   
    pprint.pprint(serv_d_d)


    print("--- --- 50. Write result into json")    
    with open(_conf_d["service_report_file_json"], 'w') as f:
      json.dump(serv_d_d, f, sort_keys = True, indent = 4, ensure_ascii = False)    
    

    print("--- --- 60. Write result into csv")    
    helper.write_list_of_dicst_into_csv(serv_d_l, _conf_d["service_report_file_csv"])  
    

    print("--- --- 70. Summmary")    
    print("Gateways data collected and stored into:")
    print("   - "+_conf_d["service_report_file_json"])
    print("   - "+_conf_d["service_report_file_csv"])    


  print("### End "+title+"###")  