#!/usr/bin/env python
import logging
import sys
import os
from trace2proda.app import Sync
from prodang.client import Client

logger = logging.getLogger(__name__)


def main():
    logging.root.setLevel(logging.DEBUG)
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting main app")
    #sys.argv.append("-v")
    sync = Sync(sys.argv)
    logger.warning(sync.get_conf())
    lib = 'dll\\prodllng.dll'
    lib  = os.path.abspath(lib)
    #print lib, os.path.exists(lib)
    client = Client(lib)
    logger.info("client created")
    client.db_connect(user="prodang", password="wabco", database="proda")
    
    client.disconnect()
    
    print "PL OK"

if __name__ == "__main__":
    sys.exit(main())