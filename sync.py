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
    print "system with id 2:", client.get_system(2)
    print "Identification: ", client.identify_me("M40", "4154064040", 0, 0)
    print "get_production_lines:", client.get_production_lines()
    print "production_line with id 2:", client.get_production_line(2)
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
