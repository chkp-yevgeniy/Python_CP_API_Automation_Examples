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
import paramiko

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
  title="Module to excute cmd on gateways"

  print("### Start "+title+"###") 
  

  print("--- --- 10. Read file with tcp services to be configured")   
  gws_l=helper.read_yaml_file(_conf_d["gws_to_access_via_ssh_yml"])
  cmds_l=helper.read_yaml_file("vars/commands.yml")
  print("Gateways to be configured: ")
  pprint.pprint(gws_l)     
  pprint.pprint(cmds_l)     

  print("--- --- 20. Iterate over gateways and commands")   
  for gw_d in gws_l:
    # Establish ssh session
    print("--- --- SSH to the gateway: "+str(gw_d))
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(gw_d["ip"],"22","admin", _conf_d["ssh_pwd"])

    for cmd_d in cmds_l:
      print("Run following command via ssh: "+cmd_d["cmd"])      
      stdin,stdout,stderr=ssh.exec_command(cmd_d["cmd"])
      outlines=stdout.readlines()
      resp=''.join(outlines)
      print(resp)

  print("### End "+title+"###")  
