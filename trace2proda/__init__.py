"""
The PLC Python library.
"""
__version__ = '0.0.2'
AUTHOR = "Piotr Wilkosz"
EMAIL = "Piotr.Wilkosz@gmail.com"
NAME = "trace2proda"

import logging
import tempfile
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .helpers import parse_config, parse_args
SQLALCHEMY_DATABASE_URI_PREFIX = 'sqlite:///'


logger = logging.getLogger(__package__.ljust(12)[:12])

_opts, _args = parse_args()
_config = {}
try:
    _config['dbfile'] = parse_config(_opts.config)['main']['dbfile'][0]
except Exception, e:
    _config['dbfile'] = tempfile.gettempdir() + os.sep + 'plc_temp.sqlite'

db_connection_string = SQLALCHEMY_DATABASE_URI_PREFIX + _config['dbfile']

_app = Flask(__name__)
_app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(_app)

db.create_all()
db.session.commit()