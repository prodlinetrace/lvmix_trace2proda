import logging
from .helpers import parse_config, parse_args
from trace2proda.models import *
import tempfile
import csv
import os
import subprocess
import datetime

logger = logging.getLogger(__name__)


class Sync(object):

    """
    Statusy Trace:
        0 - UNDEFINED
        1 - OK
        2 - NOK
        4 - NOTAVAILABLE
        5 - REPEATEDOK
        6 - REPEATEDNOK
        9 - WAITINIG
        10 - INTERRUPTED
        11 - REPEATEDINTERRUPTED
        99 - VALUEERROR

    Statusy WABCO:
        0 - NOK
        1 - OK
        2 - w trakcie produkcji
        3 - w trakcie produkcji powtorka
        5 - OK powtorzony
        6 - NOK powtorzony
        10 - przerwany test
        11 - przerwany powtorzony
        1000 - nie okreslony
        Dodatkowo 100 + powyzsza wartosc dla 'testowania' stanowiska - aby nie uwzgledniac w statystykach. Czyli np. sprawdzamy reaklamacje i chcemy zapisac wyniki ale nie chcemy wplywac na wskazniki
    """
    STATUS_CODES = [
        {"result": "UNDEFINED", "desc": "status undefined (not present in database)", "wabco": 1000, "trace": 0},
        {"result": "OK", "desc": "Status ok", "wabco": 1, "trace": 1},
        {"result": "NOK", "desc": "Status not ok", "wabco": 0, "trace": 2},
        {"result": "NOTAVAILABLE", "desc": "Not present in given type", "wabco": 4, "trace": 4},
        {"result": "REPEATEDOK", "desc": "Repeated test was ok", "wabco": 5, "trace": 5},
        {"result": "REPEATEDNOK", "desc": "Repeated test was not ok", "wabco": 6, "trace": 6},
        {"result": "WAITING", "desc": "status reset - PLC set status to 'WAITING' and waiting for PC response", "wabco": 9, "trace": 9},
        {"result": "INTERRUPTED", "desc": "Test was interrupted", "wabco": 10, "trace": 10},
        {"result": "REPEATEDINTERRUPTED", "desc": "Repeated test was interrupted", "wabco": 11, "trace": 11},
        {"result": "VALUEERROR", "desc": "Faulty value was passed. Unable to process data.", "wabco": 99, "trace": 99},
    ]

    def __init__(self, argv, loglevel=logging.INFO):
        self.sync_success_count = 0
        self.sync_failed_count = 0
        self.time_started = datetime.datetime.now()
        self._argv = argv
        self._opts, self._args = parse_args(self._argv)
        self.cleanup = False

        self.logger = logging.getLogger(__name__.ljust(24)[:24])
        self.logger.setLevel(logging.DEBUG)

        # parse config file
        self.logger.info("Using config file: {cfg}.".format(cfg=self._opts.config))
        self._config = parse_config(self._opts.config)
        #_fh = TimedRotatingFileHandler(self._config['main']['logfile'][0], when="MIDNIGHT", interval=1, backupCount=30)
        _fh = logging.FileHandler(self._config['main']['logfile'][0])
        _fh.setLevel(logging.DEBUG)
        _ch = logging.StreamHandler()
        _ch.setLevel(logging.INFO)

        if self._opts.quiet:
            # log errors to console
            _ch.setLevel(logging.ERROR)
            # log INFO+ to file
            _fh.setLevel(logging.INFO)

        if self._opts.verbose:
            self.logger.setLevel(logging.DEBUG)
            # log INFO+ to console
            _ch.setLevel(logging.DEBUG)
            # log DEBUG+ to file
            _fh.setLevel(logging.DEBUG)

        _fh.setFormatter(logging.Formatter('%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s'))
        _ch.setFormatter(logging.Formatter('%(name)s - %(levelname)8s - %(message)s'))
        self.logger.addHandler(_fh)
        self.logger.addHandler(_ch)
        self.logger.info("Using DB file: {db}".format(db=self._config['main']['dbfile'][0]))

        # cleanup (tmp csv handling)
        cleanup = self._config['main']['cleanup'][0]
        if int(cleanup) == 0:
            self.cleanup = False

        if int(cleanup) == 1:
            self.cleanup = True

        # product timeout in minutes (sync will be triggered once product will not reach station 55 within timeout.)
        self.product_timeout = 480
        if 'product_timeout' in self._config['main']:
            self.product_timeout = int(self._config['main']['product_timeout'][0])

    def get_conf(self):
        return self._config

    def get_conf_file_name(self):
        return self._opts.config

    def tace_to_wabco_status(self, st):
        """
        translates trace status code to wabco status code
        """

        for code in Sync.STATUS_CODES:
            if st == code['trace']:
                return code['wabco']
        return st

    def wabco_to_trace_status(self, st):
        """
        translates wabco status code to trace status code
        """

        for code in Sync.STATUS_CODES:
            if st == code['wabco']:
                return code['trace']
        return st

    def get_product_station_status(self, wabco_id, serial, station_id):
        # wabco_id = '4640062010'
        # serial = '000024'
        # station_id = 11
        item = Product.query.filter_by(type=wabco_id).filter_by(serial=serial).first()

        st = 1000  # set status to undefined first
        result = 0 # Test step value result - set to failed. Result has to be either 0 (NOK) or 1 (OK).
        for status in item.statuses.filter_by(station_id=station_id).all():
            st = status.status
            # set result to ok - in case station status is ok or repeatedok
            if st == 1 or st == 5:
                result = 1

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

        st = self.tace_to_wabco_status(st)

        return st, results

    def product_sync(self, wabco_id, serial):
        if wabco_id == "0":
            return 0

        if wabco_id in self._config:
            msg = "wabco_id: {wabco_id} found in config file: {config_file}".format(wabco_id=wabco_id, config_file=self.get_conf_file_name())
            self.logger.debug(msg)
            is_active = int(self._config[wabco_id]['active'][0])
            if is_active != 1:
                msg = "wabco_id: {wabco_id} is not set to active in: {config_file}".format(wabco_id=wabco_id, config_file=self.get_conf_file_name())
                self.logger.warn(msg)
                return 130
        else:
            msg = "unable to find wabco_id: {wabco_id} in config file: {config_file}. Need to skip it. Sorry!".format(wabco_id=wabco_id, config_file=self.get_conf_file_name())
            self.logger.error(msg)
            return 120

        csv_file = self.generate_csv_file(wabco_id, serial)
        if os.path.exists(csv_file):
            self.logger.debug("psark csv file generated: {csv_file}".format(csv_file=csv_file))
        else:
            self.logger.error("unable to find psark csv file generated: {csv_file}".format(csv_file=csv_file))
            return 2

        return self.run_psark(wabco_id, serial, csv_file)

    def generate_csv_file(self, wabco_id, serial):
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

            self.logger.debug("TS found in db. WI: {wabco_id} SN: {serial} TS_ID: {ts_id} TS_DESC: {ts_desc} ST: {status} TV: {tv}".format(wabco_id=wabco_id, serial=serial, ts_id=ts_id, ts_desc=ts_desc, status=status, tv=tv))

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
        self.logger.info("Running command: {cmd}".format(cmd=" ".join(cmd)))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()

        self.logger.debug(out)

        if self.cleanup:
            os.unlink(csv_file)
            self.logger.debug("CSV file removed: {csv}".format(csv=csv_file))
        else:
            self.logger.warn("CSV file not removed: {csv}".format(csv=csv_file))

        return p.returncode

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

        """
        Osobiscie sklanialem sie w strone nastepujacego rozwiazania:
        - zawor przeszedl stacje 55 - wyzwalaj synchronizacje
        - Jezeli status montazu na dowolnej stacji jest NOK - montaz zostaje przerwany - wyzwalaj synchronizacje
        - jezeli status montazu zaworu na dowolnej stacji jest OK wstrzymaj sie z syncronizacja danych do momentu az zawor dotrze do stacji 55.
        - jezeli status montazu zaworu na dowolnej stacji jest OK i zawor nie przeszedl przez stacje 55 w ciagu 24h - cos jest nie tak - wyzwalaj synchronizacje.

        """
        #candidates = Product.query.filter_by(prodasync=0).order_by(Product.date_added).filter_by(type="4640062010").all()  # TEST: limit to test type only
        candidates = Product.query.filter_by(prodasync=0).order_by(Product.date_added).all()
        for candidate in candidates:
            last_status = candidate.statuses.order_by(Status.id.desc()).first()

            # product just passed station 55 - trigger sync
            if last_status is None:
                self.logger.warn("Product: {product} has no status stored.".format(product=candidate.id))
                continue

            if last_status.station_id == 55:
                candidate.prodasync = 1
                self.logger.debug("Product: {product} set as ready to sync as it just passed station 55.".format(product=candidate.id))
                continue

            # if last status is NOK set ready to sync.
            if last_status.status == 2:
                candidate.prodasync = 1
                self.logger.debug("Product: {product} set as ready to sync due to last status set to NOK.".format(product=candidate.id))
                continue

            # product status is OK but it did not reached station 55 within 24h.
            try:
                last_status_update = datetime.datetime.now() - datetime.datetime.strptime(last_status.date_time, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError, e:
                self.logger.error("Unable to convert date: {date} with format '%Y-%m-%d %H:%M:%S.%f'. Set to timeout".format(date=last_status.date_time))
                last_status_update = datetime.datetime.now() - datetime.datetime(2015, 1, 1)

            if last_status_update.total_seconds() / 60 > self.product_timeout:
                candidate.prodasync = 1
                self.logger.debug("Product: {product} set as ready to sync as it did not reached station 55 within {timeout} minutes.".format(product=candidate.id, timeout=self.product_timeout))
                continue

            # not yet ready to sync
            self.logger.debug("Product: {product} is not yet ready to sync.".format(product=candidate.id))

        # store db session modifications to the file.
        db.session.commit()
        return 0

    def sync_all_products(self):
        #wabco_id = '4640062010'
        # prodasync column description
        # 0 - default
        # 1 - ready to sync - should be set once assembly is complete
        # 2 - sync completed successfully
        # 3 - sync failed.

        items = Product.query.filter_by(prodasync=1).order_by(Product.date_added).all()
        self.logger.info("Found: {number} products to sync".format(number=len(items)))
        for item in items:
            self.logger.info("Starting sync of: {id} PT: {type} SN: {sn} PRODA_SYNC_STAT: {prodasync}".format(id=item.id, type=item.type, sn=item.serial, prodasync=item.prodasync))
            status = self.product_sync(item.type, item.serial)
            if status == 0:
                self.sync_success_count += 1
                item.prodasync = 2
                self.logger.info("Completed sync of: {id} PT: {type} SN: {sn}. Sync Status: {status}".format(id=item.id, type=item.type, sn=item.serial, status=status))
            else:
                self.sync_failed_count += 1
                item.prodasync = 3
                self.logger.error("Failed sync of: {id} PT: {type} SN: {sn}. Sync Status: {status}".format(id=item.id, type=item.type, sn=item.serial, status=status))
            db.session.commit()

        db.session.commit()
        self.logger.info("Sync of {number} products finished in {time}. Stats: {failed} failed / {success} succeed.".format(number=len(items), failed=self.sync_failed_count, success=self.sync_success_count, time=datetime.datetime.now()-self.time_started))

        return 0
