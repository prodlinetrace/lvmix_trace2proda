import logging
from .helpers import parse_config, parse_args
from trace2proda.models import *
import tempfile
import csv
import os
import subprocess

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
            logging.root.addHandler(_ch)


        _fh.setFormatter(logging.Formatter('%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s'))
        _ch.setFormatter(logging.Formatter('%(name)s - %(levelname)8s - %(message)s'))
        # logger.addHandler(_fh)
        logging.root.addHandler(_fh)

    def get_conf(self):
        return self._config

    def get_conf_file_name(self):
        return self._opts.config

    def tace_to_wabco_status(self, st):
        """
        Statusy WABCO:
        0 – NOK
        1 – OK
        2 – w trakcie produkcji
        3 – w trakcie produkcji powtorka
        5 – OK powtorzony
        6 – NOK powtorzony
        10 – przerwany test
        11 – przerwany powtórzony
        1000 – nie okreslony
        Dodatkowo 100 + powyzsza wartosc dla "testowania" stanowiska – aby nie uwzgledniac w statystykach. Czyli np. sprawdzamy reaklamacje i chcemy zapisac wyniki ale nie chcemy wplywac na wskazniki
        """
        # TODO: implement me

        return st

    def wabco_to_trace_status(self, st):
        """
        Statusy Trace:
            STATION_STATUS_CODES = {
            0: {"result": "UNDEFINED", "desc": "status undefined (not present in database)"},
            1: {"result": "OK", "desc": "Status ok"},
            2: {"result": "NOK", "desc": "Status not ok"},
            4: {"result": "NOTAVAILABLE", "desc": "Not present in given type"},
            5: {"result": "REPEATEDOK", "desc": "Repeated test was ok"},
            6: {"result": "REPEATEDNOK", "desc": "Repeated test was not ok"},
            9: {"result": "WAITING", "desc": "status reset - PLC set status to 'WAITING' and waiting for PC response"},
            10: {"result": "INTERRUPTED", "desc": "Test was interrupted"},
            11: {"result": "REPEATEDINTERRUPTED", "desc": "Repeated test was interrupted"},
            99: {"result": "VALUEERROR", "desc": "Faulty value was passed. Unable to process data."},
        }
        """
        #TODO: implement me

        return st

    def get_product_station_status(self, wabco_id, serial, station_id):
        # wabco_id = '4640062010'
        # serial = '000024'
        # station_id = 11
        item = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()

        st = 1000  # set status to undefined first
        result = 0 # Test step result - set to failed
        for status in item.statuses.filter_by(station_id=station_id).all():
            st = status.status
            # set result to ok - in case station status is ok or repeatedok
            if st == 1 or st == 5:
                result = 1

        # TODO implement translation from traceabitity to proda status codes.
        st = self.tace_to_wabco_status(st)

        return st, [result]

    def get_product_operation_data(self, wabco_id, serial, operation_id):
        # wabco_id = '4640062010'
        # serial = '000024'
        # operation_id = 1480
        item = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()

        st = 1000  # set status to undefined first
        results = [0,0,0]
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
        st = self.tace_to_wabco_status(st)

        return st, results

    def generate_csv_file(self, wabco_id, serial):
        if wabco_id in self._config:
            msg = "wabco_id: {wabco_id} found in config file: {config_file}".format(wabco_id=wabco_id, config_file=self.get_conf_file_name())
            logger.info(msg)
        else:
            msg = "unable to find wabco_id: {wabco_id} in config file: {config_file}. Need to skip it. Sorry!".format(wabco_id=wabco_id, config_file=self.get_conf_file_name())
            logger.error(msg)
            #return 1

        csv_file_name = tempfile.mktemp(suffix=".csv", prefix="psark-{wid}-{sn}-".format(wid=wabco_id, sn=serial))

        test_steps = self._config[wabco_id]['proda_sequence']
        for ts in test_steps:
            ts_cfg = self._config[ts]
            ts_type = ts_cfg['type'][0]
            ts_name = ts_cfg['name'][0]
            ts_desc = ts_cfg['description'][0]
            ts_id = int(ts_cfg['id'][0])
            ts_tv_count = int(ts_cfg['test_values'][0])

            status = -1
            tvs = [0,0,0]
            if ts_type == 'status':
                status, tvs = self.get_product_station_status(wabco_id, serial, ts_id)
            if ts_type == 'operation':
                status, tvs= self.get_product_operation_data(wabco_id, serial, ts_id)
            tv = tvs[:ts_tv_count]

            logger.info("TS found in db. WI: {wabco_id} SN: {serial} TS_ID: {ts_id} TS_DESC: {ts_desc} ST: {status} TV: {tv}".format(wabco_id=wabco_id, serial=serial, ts_id=ts_id, ts_desc=ts_desc, status=status, tv=tv))

            with open(csv_file_name, 'ab') as csvfile:
                result_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                result_writer.writerow([status] + tv)

        return csv_file_name

    def run_psark(self, wabco_id, serial, csv_file):
        psark_exe = self._config['main']['psark'][0]
        db_user = self._config['main']['db_user'][0]
        db_pass = self._config['main']['db_pass'][0]
        db_name = self._config['main']['db_name'][0]
        cmd = [psark_exe, '-c', 'csv_feed', '-f', csv_file, '-u', db_user, '-p', db_pass, '-d', db_name, '-w', wabco_id, '-s', serial]
        logger.info("Running command: {cmd}".format(cmd=" ".join(cmd)))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err_code = p.communicate()

        logger.info(out)
        return err_code

    def product_sync(self, wabco_id, serial):
        csv_file = self.generate_csv_file(wabco_id, serial)
        if os.path.exists(csv_file):
            logger.info("psark csv file generated: {csv_file}".format(csv_file=csv_file))
        else:
            logger.error("unable to find psark csv file generated: {csv_file}".format(csv_file=csv_file))
            return 2

        return self.run_psark(wabco_id, serial, csv_file)

    def prepare_products_for_proda_sync(self):
        """
        This function iterates over database and finds products that finished assembly process.
        Such products are getting prodasync flag set to 1.
        Both failed and successully completed products get synced.
        Only products with prodasyncflag==0 should be considered.
        Products with prodasync flag set to 1 are processed by sync_all_products method.

        # prodasync flag values
        # 0 - default
        # 1 - ready to sync - should be set once assembly is complete
        # 2 - sync completed successfully
        # 3 - sync failed.

        """
        return 0


    def sync_all_products(self):
        #wabco_id = '4640062010'
        # prodasync column description
        # 0 - default
        # 1 - ready to sync - should be set once assembly is complete
        # 2 - sync completed successfully
        # 3 - sync failed.

        items = Product.query.filter_by(prodasync=1).order_by(Product.date_added).all()
        logger.info("Found: {number} products to sync".format(number=len(items)))
        for item in items:
            logger.info("Starting sync of: {id} PT: {type} SN: {sn} PRODA_SYNC_STAT: {prodasync}".format(id=item.id, type=item.type, sn=item.serial, prodasync=item.prodasync))
            status = self.product_sync(item.type, item.serial)
            logger.info("Finishing sync of: {id} PT: {type} SN: {sn} NEW Status: {status}".format(id=item.id, type=item.type, sn=item.serial, status=status))
            # TODO SET status depending on psark return code. Make sure that psark handles return codes correctly.
            item.prodasync = 2 # does not work?
