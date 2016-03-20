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
    logger.info("Proda Sync Program Started")
    logger.info("Starting main app")
    sync = Sync(sys.argv, loglevel=logging.INFO)
    sync.prepare_products_for_proda_sync()
    sync.sync_all_products()
    logger.info("Proda Sync Program Finished")


if __name__ == "__main__":
    sys.exit(main())
