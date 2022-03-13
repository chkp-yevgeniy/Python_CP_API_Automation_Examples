
#!/usr/local/bin/python3.7
#
# (c) 2021 Check Point Software Technologies
#
#
# VER   DATE            WHO                     WHAT
#------------------------------------------------------------------------------
# v1.0 16.08.2021   Yevgeniy Yeryomin       Start first lines of code

#import pprint
import sys, os
import os.path as path
from argparse import ArgumentParser
import pathlib
from pathlib import Path
from schema import Schema, And, Use, Optional, SchemaError
import pprint
import copy
from iteration_utilities import flatten

# Get project path
project_path=pathlib.Path().absolute()
#print("project_path: "+str(project_path))

# Set sys path
#sys.path.append(os.path.abspath(os.path.join(project_path, 'helpers')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'src')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'src/helpers')))
sys.path.append(os.path.abspath(os.path.join(project_path, 'src/fetch_dyn_objs')))
#print("sys.path: "+str(sys.path))

import helper
import helper_io

global log

def merge_targets_policies_lists(_domains_targs_l, _domains_pol_l, _data_d, log):      
  ### Merge following:
  # TARGETS:
  # - domain_name: "TEST"
  #   targets: 
  #     - "fra-jhf-test-sg1-fw"
  # POLICIES:
  # - domain_name: "TEST"
  #   policies: 
  #     - "64K-migration"
  #     - "dcsgp-test-oe1-int"
  #     - "eu-ibm-test-oe-int"
  # - domain_name: "WIFI"
  #   policies: 
  #     - "domains_pdp"
  # Clean export file
  helper.delete_file(_data_d["collected_data"]["domains_targets_policies_merged_json"])
  # Initiate lists in case they are None
  if not _domains_targs_l: _domains_targs_l=[]
  if not _domains_pol_l: _domains_pol_l=[]
  # Get domain_names list
  domains_l=[]
  domains_l.extend([x["domain_name"] for x in _domains_targs_l])
  domains_l.extend([x["domain_name"] for x in _domains_pol_l])
  domains_l=list(set(domains_l))  
  # get domains dicts list
  domains_targs_pol_l=[{"domain_name": x} for x in domains_l]      
  # create new list of dicts   
  for domain_d in domains_targs_pol_l:        
    domain_d["targets"]=[x["targets"] for x in _domains_targs_l if x["domain_name"]==domain_d["domain_name"]]
    domain_d["policies"]=[x["policies"] for x in _domains_pol_l if x["domain_name"]==domain_d["domain_name"]]
    domain_d["targets"]=list(flatten(domain_d["targets"]))    
    domain_d["policies"]=list(flatten(domain_d["policies"]))    
  #pprint.pprint(domains_targs_pol_l)     
  helper_io.write_json_file(domains_targs_pol_l, _data_d["collected_data"]["domains_targets_policies_merged_json"])    
  log.info("Merged data written into: "+_data_d["collected_data"]["domains_targets_policies_merged_json"])  

def verify_data_schema_wrapper(domains_targs_l, _data_d):  
  verification_ok=True
  schema_domains_targets = Schema([{
      'domain_name': And(Use(str)),
      'targets': [And(Use(str))]        
  }])

  if not domains_targs_l:
    log.info("Domains targets list is empty: "+_data_d["input"]["domains_targets_to_be_instld"])
    return True
  
  if not helper.data_schema_check(schema_domains_targets, domains_targs_l):
    verification_ok=False    
    log.error("Data scheme verification failed for: "+_data_d["input"]["domains_targets_to_be_instld"])
    log.error("Data must have following structure: ")
    log.error(pprint.pprint(schema_domains_targets))
    pprint.pprint(schema_domains_targets.json_schema)    
    exit()    
  else: 
    log.info("Data schema OK for: "+_data_d["input"]["domains_targets_to_be_instld"])
  return verification_ok

def check_input_data_is_not_empty_OLD(_domains_targs_l, _pol_install_profile_l):
  # pprint.pprint(_domains_targs_l) 
  # exit()
  relevant_data_not_emty=True
  no_new_targets=False
  no_policies_targets_in_inst_prof=False
  if not _domains_targs_l and not _pol_install_profile_l:
    relevant_data_not_emty=False
    return relevant_data_not_emty

  # in _domains_targs_l, check if there are gateways
  if not _domains_targs_l: 
    no_new_targets=True
  elif not [x["targets"] for x in _domains_targs_l]:
    no_new_targets=True
    
  # in _pol_install_profile_d, chek if there are policies and gateways   
  if not _pol_install_profile_l:
    no_policies_targets_in_inst_prof=True
  elif not [x["policies"] for x in _pol_install_profile_l]:
    no_policies_targets_in_inst_prof=True

  if no_new_targets and no_policies_targets_in_inst_prof:
    relevant_data_not_emty=False

  #targets_l=
  return relevant_data_not_emty

def check_input_data_is_not_empty(_domains_targs_pol_l, _pol_install_profile_d):
  # pprint.pprint(_domains_targs_pol_l) 
  # exit()
  relevant_data_not_empty=True
  no_new_targets=False
  no_new_policies=False
  no_policies_targets_in_inst_prof=False
  if not _domains_targs_pol_l and not _pol_install_profile_d:
    relevant_data_not_empty=False
    return relevant_data_not_empty

  # in _domains_targs_pol_l, check if there are gateways
  if not _domains_targs_pol_l: 
    no_new_targets=True
  elif not [x["targets"] for x in _domains_targs_pol_l]:
    no_new_targets=True
  elif not [x["policies"] for x in _domains_targs_pol_l]:
    no_new_policies=True
    
    
  pol_install_profile_l=[]  
  if _pol_install_profile_d and "objects" in _pol_install_profile_d:
    pol_install_profile_l=_pol_install_profile_d["objects"]
        
  # in _pol_install_profile_d, chek if there are policies and gateways   
  if not pol_install_profile_l:
    no_policies_targets_in_inst_prof=True
  elif not [x["objects"] for x in pol_install_profile_l]:
    no_policies_targets_in_inst_prof=True

  if no_new_targets and no_new_policies and no_policies_targets_in_inst_prof:
    relevant_data_not_empty=False

  #targets_l=
  return relevant_data_not_empty

def get_rendered_conf_d_wapper(_cli_d, _conf_d, _cur_date_time_YMD_HMS):   
  # Prepare rendering dict
  rend_d={}    
  if _cli_d["dev_run"]==True:
    rend_d["env"]="dev"
  else:
    rend_d["env"]="prod"          
  rend_d["project_path"]=project_path
  rend_d["date_time"]=_cur_date_time_YMD_HMS
  #rend_d["state_folder"]=conf_d["state_folder"]
  
  # Get rendered config    
  conf_d=helper.get_rendered_conf_d(_cli_d["configfile"], _conf_d, rend_d)
  #pprint.pprint(conf_d)
  
  return conf_d

def read_cli_args():
  #print("Read cli arguments.")
  cli_d={}  
  parser = ArgumentParser()
  parser.add_argument('-c', "--config_file", dest="config_file", required=True, help="Configuration ini file.")    
  parser.add_argument('-dev', "--development_run", dest="development_run", help="Development run. It means a test run usually during development phase. Logs and reports during the test run will be stored in dev or prod directories.", action="store_true")     
  #parser.add_argument('-apply', "--apply", dest="apply", help="Apply target gateways configuration in case of deviation with current (collected) config.", action="store_true")         
  parser.add_argument('-do_not_collect_mds_domains', "--do_not_collect_mds_domains", dest="do_not_collect_mds_domains", help="Do not collect mds domains. Use instead information collected during previous run. It will save some minutes.", action="store_true")     
  parser.add_argument('-do_not_collect_audit_logs', "--do_not_collect_audit_logs", dest="do_not_collect_audit_logs", help="Do not collect audit logs from MDSs. Use instead information collected during previous run. It will save some minutes.", action="store_true")     
  #parser.add_argument('-do_not_collect_policies', "--do_not_collect_policies", dest="do_not_collect_policies", help="Do not collect policies. Use instead information collected during previous run. It will save some minutes.", action="store_true")     
  parser.add_argument('-do_not_get_inst_pol_gws_mapping', "--do_not_get_inst_pol_gws_mapping", dest="do_not_get_inst_pol_gws_mapping", help="Do not get intalled policies and gateways mapping from MDSs database. Use instead information collected during previous run.", action="store_true")     
  parser.add_argument('-mdss_limit', "--mdss_limit", dest="mdss_limit", type=int, help="Limit number of MDSs to be processed on. This argument is useful for development phase.")
  parser.add_argument('-domains_limit', "--domains_limit", dest="domains_limit", type=int, help="Limit number of domains to be processed on. This argument is useful for development phase.")
  parser.add_argument('-do_not_get_modified_policies', "--do_not_get_modified_policies", dest="do_not_get_modified_policies", help="Don't get changed and not yet installed policies from MDS.", action="store_true")     
  parser.add_argument("-process_on_changed_policies", "--process_on_changed_policies", dest="process_on_changed_policies", help="Process on changed policies.", action="store_true")     
  parser.add_argument("-process_on_changed_targets", "--process_on_changed_targets", dest="process_on_changed_targets", help="Process on changed targets.", action="store_true")       
  parser.add_argument('-install_policies', "--install_policies", dest="install_policies", help="Install policies on gateways. If this flag not set, perform a dry run.", action="store_true")
  cli_args = parser.parse_args()    
     
  if not cli_args.config_file: 
    parser.error("Please provide configfile")  
  if cli_args.domains_limit and cli_args.domains_limit<0:
    parser.error("domains_limit must be positiv integer")  
    
  # Process arg, put them into dict
  cli_d["configfile"]=cli_args.config_file    
  cli_d["dev_run"]=cli_args.development_run  
  #cli_d["apply"]=cli_args.apply      
    
  cli_d["do_not_collect_mds_domains"]=cli_args.do_not_collect_mds_domains  
  cli_d["do_not_collect_audit_logs"]=cli_args.do_not_collect_audit_logs  
  # cli_d["do_not_collect_policies"]=cli_args.do_not_collect_policies    
  cli_d["do_not_get_inst_pol_gws_mapping"]=cli_args.do_not_get_inst_pol_gws_mapping
  cli_d["mdss_limit"]=cli_args.mdss_limit  
  cli_d["domains_limit"]=cli_args.domains_limit  
  cli_d["do_not_get_modified_policies"]=cli_args.do_not_get_modified_policies  
  cli_d["process_on_changed_policies"]=cli_args.process_on_changed_policies    
  cli_d["process_on_changed_targets"]=cli_args.process_on_changed_targets    
  cli_d["install_policies"]=cli_args.install_policies    
    
  return cli_d

def print_conf(_conf_d):
  log.info("Configuration data:")       
  for k, v in _conf_d.items():
    if type(v)==dict:
      log.info(" - {:24}".format(k))   
      for _k, _v in v.items():
        log.info("    - {:30} {}".format(_k, str(_v)))  
    else: 
      log.info(" - {:30} {}".format(k, str(v)))      


