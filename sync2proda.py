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

def get_proda_id(trace_id):
    result = T2P.query.filter_by(trace_id = trace_id).first()
    #print result
    if result is not None:
        return result.proda_id;
    else:
        return 0

def main():
    print "Proda Sync Program Started"
    logging.root.setLevel(logging.DEBUG)
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting main app")
    sys.argv.append("-v")
    sync = Sync(sys.argv)
    #conf = sync.get_conf()
    #print conf
    #logger.warning(sync.get_conf())
    wabco_id='4640062010'
    serial = '000024'

    sync.product_sync(wabco_id, serial)
    #return 2
    #proda_sync(wabco_id=wabco_id, serial = serial)

    print "Proda Sync Program Finished"

if __name__ == "__main__":
    sys.exit(main())
