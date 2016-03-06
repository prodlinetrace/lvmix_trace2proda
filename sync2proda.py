#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
import sys
import os
import six
from trace2proda.app import Sync
#from prodang.client import Client
#from trace2proda import app, db
#from trace2proda.helpers import parse_config, parse_args
from trace2proda.models import *


logger = logging.getLogger(__name__)


def init_db():
    pass
    #print db

def get_proda_id(trace_id):
    result = T2P.query.filter_by(trace_id = trace_id).first()
    #print result
    if result is not None:
        return result.proda_id;
    else:
        return 0

def get_product_station_status(wabco_id, serial, station_id):
    # wabco_id = '4640062010'
    # serial = '000024'
    # station_id = 11
    item = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()

    st = -1  # set status to undefined first
    for status in item.statuses.filter_by(station_id=station_id).all():
        st = status.status

    # TODO implement translation from traceabitity to proda status codes.
    return st, st

def get_product_operation_data(wabco_id, serial, operation_id):
    # wabco_id = '4640062010'
    # serial = '000024'
    # operation_id = 1480
    item = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()

    st = -1  # set status to undefined first
    for operation in item.operations.filter_by(operation_type_id=operation_id).all():
        st = operation.operation_status_id
        results = [0,0,0]
        if not operation.result_3 == operation.result_3_max == operation.result_3_min == 0:
            results.insert(0,operation.result_3)
        if not operation.result_2 == operation.result_2_max == operation.result_2_min == 0:
            results.insert(0,operation.result_2)
        if not operation.result_1 == operation.result_1_max == operation.result_1_min == 0:
            results.insert(0,operation.result_1)

    # TODO implement translation from traceabitity to proda status codes.
    return st, results


def proda_sync(wabco_id, serial):
    # wabco_id = '4640062010'
    # serial = '000024'
    # Sync.

    result = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()
    item = result
    for status in item.statuses.all():
        pass
        #print status
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

        #print  "Type ID: ", operation.operation_type.id, "Proda_TS_ID:", operation.operation_type.proda_id, "Type Name: ", operation.operation_type.name, "Status ID: ", operation.operation_status.id, "Proda Status ID: ", operation.operation_status.proda_id, "Result 1", results[0], "Result 2", results[1], "Result 3:", results[2]


def main():
    print "Proda Sync Program Started"
    logging.root.setLevel(logging.DEBUG)
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting main app")
    #init_db()

    #sys.argv.append("-v")
    sync = Sync(sys.argv)
    conf = sync.get_conf()
    print conf
    #logger.warning(sync.get_conf())
    wabco_id='4640062010'
    serial = '000024'

    #wabco_id="54_sta"
#    if "wabcoid_{wabco_id}".format(wabco_id=wabco_id) not in conf:
    if wabco_id in conf:
        msg = "wabco_id: {wabco_id} found in config file: {config_file}".format(wabco_id=wabco_id, config_file=sync.get_conf_file_name())
        logger.error(msg)
        print msg
    else:
        msg = "unable to find wabco_id: {wabco_id} in config file: {config_file}. Need to skip it. Sorry!".format(wabco_id=wabco_id, config_file=sync.get_conf_file_name())
        logger.error(msg)
        print msg
        return 1

    csv_input = []

    test_steps = conf[wabco_id]['proda_sequence']
    for ts in test_steps:
        ts_cfg = conf[ts]
        ts_type = ts_cfg['type'][0]
        ts_name = ts_cfg['name'][0]
        ts_desc = ts_cfg['description'][0]
        ts_id = int(ts_cfg['id'][0])
        ts_tv_count = int(ts_cfg['test_values'][0])

        status = -1
        tvs = [0,0,0]
        if ts_type == 'status':
            status, tvs = get_product_station_status(wabco_id, serial, ts_id)
        if ts_type == 'operation':
            status, tvs= get_product_operation_data(wabco_id, serial, ts_id)
        tv = tvs[:ts_tv_count]
        print ts_id, ts_desc, "status: ", status, "tv: ", tv, "tv_count: ", ts_tv_count

    return 2
    proda_sync(wabco_id=wabco_id, serial = serial)

    print "Proda Sync Program Finished"

if __name__ == "__main__":
    sys.exit(main())
