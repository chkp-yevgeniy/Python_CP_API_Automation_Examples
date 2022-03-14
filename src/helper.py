
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
import yaml

# Get project path
project_path=pathlib.Path().absolute()
# Set sys path
sys.path.append(os.path.abspath(os.path.join(project_path, 'src')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'libs/cp_mgmt_api_python_sdk')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'src/modules')))

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


def read_yaml_file(_filename):
  with open(_filename, 'r') as fp:
    my_dict = yaml.safe_load(fp)
  return my_dict

# Functions section end


