
#!/usr/local/bin/python3.7

# How to start:
# python3 src/<name of script>

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
# Set sys path
sys.path.append(os.path.abspath(os.path.join(project_path, 'src')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'libs/cp_mgmt_api_python_sdk')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'src/modules')))
#print("sys.path: "+str(sys.path))

# Import CP API lib
from cpapi import APIClient, APIClientArgs
import get_services_tcp
import add_services_tcp
import add_policy_packages
import get_packages
import add_rules
# import manage_users
import gws_execute_cmd


# Functions section

def write_list_of_dicst_into_csv(_my_dicts_list, _csv_file_name):
  delimiter=";"
  if _my_dicts_list:
    keys = _my_dicts_list[0].keys()
    with open(_csv_file_name, 'w', newline='') as ouput_file: 
      dict_writer=csv.DictWriter(ouput_file, keys, delimiter=delimiter)
      dict_writer.writeheader()
      dict_writer.writerows(_my_dicts_list)


def fill_api_calls_res(_api_calls_res_d_l, _api_call_d, _api_res_d_success):
  res_d={}
  res_d.update(_api_call_d)
  res_d["api_call_res"]=_api_res_d_success
  _api_calls_res_d_l.append(res_d)

# Functions section end


def main():
    
    # Timestamp
    cur_date_time_YMD_HMS=os.popen('date +%Y%m%d_%H%M%S').read().strip()      

    # Variables 
    conf_d={}
    conf_d["mgmt_ip"]="203.0.113.80"
    conf_d["mgmt_user"]="api_user"
    conf_d["mgmt_pwd"]="vpn123"
    conf_d["domain"]=""
    conf_d["reports_folder"]="collected_data"
    conf_d["report_file_json"]=os.path.join(conf_d["reports_folder"], "gws.json")
    conf_d["report_file_csv"]=os.path.join(conf_d["reports_folder"], "gws.csv")
    
    api_calls_res_d_l=[]
    
    # Set timestamp
    conf_d["report_file_json_ts"]=conf_d["report_file_json"].replace(".json", "_"+cur_date_time_YMD_HMS+".json")
    conf_d["report_file_csv_ts"]=conf_d["report_file_csv"].replace(".csv", "_"+cur_date_time_YMD_HMS+".csv")

    # List of gateways to be configurred
    conf_d["gws_list_to_be_conf"]="vars/gws.json"
    conf_d["policy_packages_yml"]="vars/policy_packages.yml"
    conf_d["rules_yml"]="vars/rules.yml"
    conf_d["users_yml"]="vars/users.yml"
    conf_d["gws_to_access_via_ssh_yml"]="vars/gws_to_access_via_ssh.yml"
    # pprint.pprint(conf_d)
    #     

    # Create folder
    newpath = 'collected_data' 
    if not os.path.exists(newpath):
      os.makedirs(newpath)

    print("### ### Start tool ### ###")


    # print("--- 10 Get services")    
    # get_services_tcp.my_main(conf_d)


    # print("--- 20 Add services")    
    # conf_d["services_tcp_yml"]="vars/services_tcp.yml"
    # add_services_tcp.my_main(conf_d)


    # print("--- 30 Get policy packages")    


    # print("--- 40 Add policy packages")    


    # print("--- 50 Add rules")    


    
    # print("--- 70 Execute cmd on gateways")    
    # gws_execute_cmd.my_main(conf_d)

    
       
if __name__ == "__main__":
    main()

