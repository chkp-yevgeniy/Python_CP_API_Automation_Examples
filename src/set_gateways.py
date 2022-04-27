
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
# print("sys.path: "+str(sys.path))

# Import CP API lib
from cpapi import APIClient, APIClientArgs


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
    # Put here ip address and credentials of your management server 
    conf_d["mgmt_ip"]=""
    conf_d["mgmt_user"]=""
    conf_d["mgmt_pwd"]=""    
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
    # pprint.pprint(conf_d)
    #     

    # Create folder
    newpath = 'collected_data' 
    if not os.path.exists(newpath):
      os.makedirs(newpath)

    print("### ### Start tool ### ###")
    
    print("--- 10 Read gateways list")
    with open(conf_d["gws_list_to_be_conf"]) as json_data:
      gws_d_d= json.load(json_data)
    pprint.pprint(gws_d_d)
    
    # Get API client objects    
    client_args = APIClientArgs(server=conf_d["mgmt_ip"], unsafe_auto_accept=True)
    with APIClient(client_args) as client:          
      #api_calls_l=_domain_d["api_calls"]
      
      # login to server:
      login_res = client.login(conf_d["mgmt_user"], conf_d["mgmt_pwd"], domain=conf_d["domain"])                
      print("--- 20. Login on target {} {} {} {}".format(conf_d["mgmt_user"], conf_d["domain"], conf_d["mgmt_ip"], str(login_res.success)))      

      print("--- 30. Iterate over list of gateways")  
      for gw_d in gws_d_d["objects"]:
        pprint.pprint(gw_d)
      
        print("--- --- 30.10 Prepare api call")
        api_call_d={}
        api_call_d["name"]="set-simple-gateway"
        api_call_d["body"]={}
        api_call_d["body"]["name"]=gw_d["name"]
        api_call_d["body"]["comments"]=gw_d["comments"]
        body_json=json.dumps(api_call_d["body"])

        print("--- --- 30.20 Execute api call on "+gw_d["name"])
        api_res_d = client.api_call(api_call_d["name"], body_json)
        #pprint.pprint(api_res_d)        
        print("API call result: "+str(api_res_d.success))        
        # Fill api_calls_res_d_l
        fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)


      print("--- 40. Execute api call PUBLISH")    
      api_call_d={}
      api_call_d["name"]="publish"
      api_call_d["body"]={}
      api_res_d = client.api_call(api_call_d["name"], "{}")
      #pprint.pprint(api_res_d)      
      # Evaluate api_call result
      print("API call result: "+str(api_res_d.success))        
      # Fill api_calls_res_d_l
      fill_api_calls_res(api_calls_res_d_l, api_call_d, api_res_d.success)
      

    print("--- 50. Process on result")    
    # Get statistics
    stats_d={}
    stats_d["api_calls_total"]=str(len(api_calls_res_d_l))
    stats_d["api_calls_successful"]=str(len([x for x in api_calls_res_d_l if x["api_call_res"]==True]))
    stats_d["api_calls_failed"]=str(len([x for x in api_calls_res_d_l if x["api_call_res"]==False]))
    print("Statistics")
    #pprint.pprint(stats_d)
    print(json.dumps(stats_d, indent=4, sort_keys=True))
    

    # print("--- Write result into json")    
    # with open(conf_d["report_file_json"], 'w') as f:
    #   json.dump(gws_d_d, f, sort_keys = True, indent = 4, ensure_ascii = False)    
    # with open(conf_d["report_file_json_ts"], 'w') as f:
    #   json.dump(gws_d_d, f, sort_keys = True, indent = 4, ensure_ascii = False)    

    # print("--- Write result into csv")    
    # write_list_of_dicst_into_csv(gws_d_l, conf_d["report_file_csv"])  
    # write_list_of_dicst_into_csv(gws_d_l, conf_d["report_file_csv_ts"])  


    print("--- 60. Summmary")    
    print("Following api calls have beed executed: ")
    # pprint.pprint(api_calls_res_d_l)
    print(json.dumps(api_calls_res_d_l, indent=4, sort_keys=True))
       
if __name__ == "__main__":
    main()

