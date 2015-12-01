#!/usr/bin/env python
import logging
import sys
from trace2proda.app import Sync

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting main app")
    #sys.argv.append("-v")
    sync = Sync(sys.argv)
    logger.warning(sync.get_conf())
    print "PL OK"

if __name__ == "__main__":
    sys.exit(main())
