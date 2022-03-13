
#!/usr/local/bin/python3.7
#
# (c) 2021 Check Point Software Technologies
#
# Tool for policy installation 
#
# 
#
# VER   DATE            WHO                     WHAT
#------------------------------------------------------------------------------
# v1.0 29.09.2021   Yevgeniy Yeryomin       Write first lines of code

# How to start:
# python3 src/main.py
# Use -h cli option to discover cli agruments

from pprint import pprint
import sys, os
import os.path as path
import logging
from pathlib import Path
import json
import pathlib
import pprint
import csv
#from argparse import ArgumentParser
# import shutil
# import re
# import pytz

# Get project path
project_path=pathlib.Path().absolute()

# Set sys path
sys.path.append(os.path.abspath(os.path.join(project_path, 'src')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'libs/cp_mgmt_api_python_sdk')))


# print("sys.path: "+str(sys.path))
# import apply
from cpapi import APIClient, APIClientArgs


def write_list_of_dicst_into_csv(_my_dicts_list, _csv_file_name):
  delimiter=";"
  if _my_dicts_list:
    keys = _my_dicts_list[0].keys()
    with open(_csv_file_name, 'w', newline='') as ouput_file: 
      dict_writer=csv.DictWriter(ouput_file, keys, delimiter=delimiter)
      dict_writer.writeheader()
      dict_writer.writerows(_my_dicts_list)


def main():
    global log        
    
    loglevel=logging.INFO
    cur_date_time_YMD_HMS=os.popen('date +%Y%m%d_%H%M%S').read().strip()  
    
    # Variables 
    conf_d={}
    conf_d["mgmt_ip"]="192.168.168.100"
    conf_d["mgmt_user"]="api_user"
    conf_d["mgmt_pwd"]="vpn123"
    conf_d["domain"]="CMA1"
    conf_d["reports_folder"]="collected_data"
    conf_d["report_file_json"]=os.path.join(conf_d["reports_folder"], "gws.json")
    conf_d["report_file_csv"]=os.path.join(conf_d["reports_folder"], "gws.csv")
    
    # Set timestamp
    conf_d["report_file_json_ts"]=conf_d["report_file_json"].replace(".json", "_"+cur_date_time_YMD_HMS+".json")
    conf_d["report_file_csv_ts"]=conf_d["report_file_csv"].replace(".csv", "_"+cur_date_time_YMD_HMS+".csv")

    # Create folder
    newpath = 'collected_data' 
    if not os.path.exists(newpath):
      os.makedirs(newpath)


    print("### ### Start tool ### ###")
    

    # Get gateways list
    
    client_args = APIClientArgs(server=conf_d["mgmt_ip"], unsafe_auto_accept=True)
    with APIClient(client_args) as client:          
      #api_calls_l=_domain_d["api_calls"]
      
      # login to server:
      login_res = client.login(conf_d["mgmt_user"], conf_d["mgmt_pwd"], domain=conf_d["domain"])    
      # _domain_d["api_login_ok"]=login_res.success  
      # _domain_d["api_calls"]=[]
      
      print("### Login on target {} {} {} {}".format(conf_d["mgmt_user"], conf_d["domain"], conf_d["mgmt_ip"], str(login_res.success)))      

      print("### Prepare api call")
      api_call_d={}
      api_call_d["name"]="show-simple-gateways"
      api_call_d["body"]={}
      api_call_d["body"]["details-level"]="full"
      api_call_d["body"]["limit"]="500"
      body_json=json.dumps(api_call_d["body"])

      print("### Execute api call")
      api_res_d = client.api_call(api_call_d["name"], body_json)
      # pprint.pprint(api_res_d)
      if api_res_d.success:
        print("   API call successfull")
      else: 
        print("   ERROR: API call failed")


    print("### Process on result")
    #pprint.pprint(api_res_d.data)
    gws_d_l=[]
    for api_res_gw_d in api_res_d.data["objects"]:
      #pprint.pprint(api_res_gw_d)
      # Put gw params into a dict
      gw_d={}
      gw_d["name"]=api_res_gw_d["name"]
      gw_d["ip"]=api_res_gw_d["ipv4-address"]
      gw_d["version"]=api_res_gw_d["version"]      
      gw_d["sic-state"]=api_res_gw_d["sic-state"]
      gw_d["fw_blade"]=api_res_gw_d["firewall"]
      gws_d_l.append(gw_d)      
    #pprint.pprint(gws_d_l)


    print("### Transform to dict and get statistics")    
    gws_d_d={}
    gws_d_d["objects"]=gws_d_l
    gws_d_d["total"]=str(len(gws_d_l))


    print("### Write result into json")    
    with open(conf_d["report_file_json"], 'w') as f:
      json.dump(gws_d_d, f, sort_keys = True, indent = 4, ensure_ascii = False)    
    with open(conf_d["report_file_json_ts"], 'w') as f:
      json.dump(gws_d_d, f, sort_keys = True, indent = 4, ensure_ascii = False)    


    print("### Write result into csv")    
    write_list_of_dicst_into_csv(gws_d_l, conf_d["report_file_csv"])  
    write_list_of_dicst_into_csv(gws_d_l, conf_d["report_file_csv_ts"])  


    print("### Summmary")    
    print("Gateways data collected and stored into:")
    print("   - "+conf_d["report_file_json"])
    print("   - "+conf_d["report_file_csv"])
    print("   - "+conf_d["report_file_json_ts"])
    print("   - "+conf_d["report_file_csv_ts"])
       
if __name__ == "__main__":
    main()

