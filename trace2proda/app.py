import logging
from .helpers import parse_config, parse_args
#from .database import Database

logger = logging.getLogger(__name__)


class Sync(object):

    def __init__(self, argv, loglevel=logging.INFO):
        self._argv = argv
        self._opts, self._args = parse_args(self._argv)

        # handle logging - set root logger level
        logging.root.setLevel(logging.INFO)
        logger = logging.getLogger(__name__.ljust(24)[:24])
        logger.setLevel(loglevel)

        # parse config file
        logger.info("Using config file {cfg}.".format(cfg=self._opts.config))
        self._config = parse_config(self._opts.config)
        #_fh = TimedRotatingFileHandler(self._config['main']['logfile'][0], when="MIDNIGHT", interval=1, backupCount=30)
        _fh = logging.FileHandler(self._config['main']['logfile'][0])
        _ch = logging.StreamHandler()

        if self._opts.quiet:
            # log errors to console
            _ch.setLevel(logging.ERROR)
            # log INFO+ to file
            _fh.setLevel(logging.INFO)

        if self._opts.verbose:
            # log INFO+ to console
            _ch.setLevel(logging.INFO)
            # log DEBUG+ to file
            _fh.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
            logging.root.setLevel(logging.DEBUG)

        _fh.setFormatter(logging.Formatter('%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s'))
        _ch.setFormatter(logging.Formatter('%(name)s - %(levelname)8s - %(message)s'))
        # logger.addHandler(_fh)
        logging.root.addHandler(_fh)

    def get_conf(self):
        return self._config

    def get_conf_file_name(self):
        return self._opts.config