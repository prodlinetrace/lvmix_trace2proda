#!/usr/bin/env python
import logging
import sys
import os
from trace2proda.app import Sync
from prodang.client import Client
from trace2proda import app, db
from trace2proda.helpers import parse_config, parse_args
from trace2proda.models import *


logger = logging.getLogger(__name__)


def init_db():
    pass
    print db

def get_proda_id(trace_id):
    result = T2P.query.filter_by(trace_id = trace_id).first()
    #print result
    if result is not None:
        return result.proda_id;
    else:
        return 0

def proda_sync(wabco_id, serial):
    #wabco_id = '4640062010'
    #serial = '000024'
    #Sync.
    
    result = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()
    item = result
    for status in item.statuses.all():
        print status
    for operation in item.operations.all():
        #print  "Type ID: ", operation.operation_type.id, "Proda TS_ID:", get_proda_id(operation.operation_type_id), "Type Name: ", operation.operation_type.name, "Status ID: ", operation.operation_status_id, "Proda Status ID: ", get_proda_id(operation.operation_status_id)
        #// skip empty / fake results
        results = [0,0,0]
        if not operation.result_3 == operation.result_3_max == operation.result_3_min == 0: 
            results.insert(0,operation.result_3)
        if not operation.result_2 == operation.result_2_max == operation.result_2_min == 0: 
            results.insert(0,operation.result_2)
        if not operation.result_1 == operation.result_1_max == operation.result_1_min == 0: 
            results.insert(0,operation.result_1)
            
        print  "Type ID: ", operation.operation_type.id, "Proda_TS_ID:", operation.operation_type.proda_id, "Type Name: ", operation.operation_type.name, "Status ID: ", operation.operation_status.id, "Proda Status ID: ", operation.operation_status.proda_id, "Result 1", results[0], "Result 2", results[1], "Result 3:", results[2]   


def main():
    print "Proda Sync Program Started"
    logging.root.setLevel(logging.DEBUG)
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting main app")  
    init_db()
    
    #sys.argv.append("-v")
    #sync = Sync(sys.argv)
    #logger.warning(sync.get_conf())
    
    proda_sync(wabco_id='4640062010', serial = '000024')
    
    print "Proda Sync Program Finished"

if __name__ == "__main__":
    sys.exit(main())
