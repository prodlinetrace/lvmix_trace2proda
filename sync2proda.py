#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
import sys
import os
import six
from trace2proda.app import Sync
from trace2proda.models import *


logger = logging.getLogger(__name__)

def main():
    logging.root.setLevel(logging.DEBUG)
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.info("Proda Sync Program Started")
    logging.info("Starting main app")
    sys.argv.append("-v")
    sync = Sync(sys.argv)
    wabco_id='4640062010'
    sync.prepare_products_for_proda_sync()
    sync.sync_all_products()
    logger.info("Proda Sync Program Finished")


if __name__ == "__main__":
    sys.exit(main())
