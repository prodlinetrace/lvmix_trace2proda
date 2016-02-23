#!/usr/bin/env python
import logging
import sys
import os
from trace2proda.app import Sync
from prodang.client import Client

logger = logging.getLogger(__name__)


def proda_test():
    lib = 'dll\\prodllng.dll'
    lib  = os.path.abspath(lib)
    #print lib, os.path.exists(lib)
    client = Client(lib)
    logger.info("client created")
    client.db_connect(user="prodang", password="wabco", database="proda")
    client.set_preference("RETRYCOUNT", 2)
    client.get_database_time()
    client.get_last_error_msg()
    client.set_language(3)
    print "last oracle error message:", client.get_last_error_msg()
    print "units:", client.get_units()
    print "languages:", client.get_languages()
    print "last oracle error message:", client.get_last_error_msg()
    print "mime types:", client.get_mime_types()
    print "systems:", client.get_systems()
    print "system with id 7:", client.get_system(7)
    print "Identification: ", client.identify_me("LV_MIX_process", "4640062010", 0, 0)
    print "production_lines:", client.get_production_lines()
    print "production_line with id 4:", client.get_production_line(4)
    print "waabco_parts:", client.get_wabco_parts()
    print "waabco_parts with id 2:", client.get_wabco_part(2)
    print "processes:", client.get_processes()
    print "process with id 1202:", client.get_process(1202)
    print "processes with wabco_part_id 2:", client.get_wabco_part_processes(wabco_part_id=2)
    print "process steps with process_id 1202:", client.get_process_steps(process_id=1202)
    print "process step with id 5:", client.get_process_step(ident=5)
    #print "process step params with process_step_id 5:", client.get_process_step_params(process_step_id=5)
    process_step_param_example = {
        'id': 8,
        'processStepId': 8,
        'unitId': 2,
        'contentId': "2",
        'previewId': "2",
        'value': 3.1415,
        'valueText': "some value in text format",
        'paramSequence': 1,
        'history': 0,
        'mdReason': "just added for test",
        'mdUser': "wilkpio",
        'mdTime': "now",
        'description': "some test description",
    }
    #print process_step_param_example['unitId']
    #client.new_process_step_param(process_step_param_example)
    #print "process step params with process_step_id 8:", client.get_process_step_params(process_step_id=8)
    print "get product:", client.get_product(wabco_part_id=3, serial_number="123459")
    #print "create product:", client.new_product(wabco_part_id=3, serial_number="123459", individual=1, comment="")
    
    client.db_disconnect()


def main():
    print "Proda Sync Program Started"
    logging.root.setLevel(logging.DEBUG)
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting main app")  
    
    #sys.argv.append("-v")
    #sync = Sync(sys.argv)
    #logger.warning(sync.get_conf())
    
    proda_test()
    
    print "Proda Sync Program Finished"

if __name__ == "__main__":
    sys.exit(main())
