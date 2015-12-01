import sys
import os
import ConfigParser
from optparse import OptionParser


def usage(name=sys.argv[0]):
    ret = """
    Usage: %s
    """ % (name)
    return ret


def parse_args(argv=sys.argv):
    parser = OptionParser(usage=usage(argv))

    cd = os.path.dirname(argv[0])
    fn = os.path.basename(argv[0])
    bn = fn.split('.')[:-1]
    conf_file = os.path.join(cd, ".".join(bn + ['conf']))

    parser.add_option("-c", "--config", help="location of config file, default: %s " % conf_file, default=conf_file)
    parser.add_option("-q", "--quiet", action="store_true", default=False, help="don't print status messages to stdout")
    parser.add_option("-v", "--verbose", action="store_true", default=False, help="verbose mode")

    opts, args = parser.parse_args()
    return opts, args


def parse_config(f):
    config = ConfigParser.RawConfigParser()
    config.read(f)
    c = {}
    for section in config.sections():
        c[section] = {}
        for option in config.options(section):
            c[section][option] = map(str.strip, config.get(section, option).split(','))

    # in case program is not installed correctly try to guess better paths
    for k in ['dbfile', 'logfile']:
        path = c['main'][k][0]
        c['main'][k][0] = os.path.abspath(path)

    return c
