from ctypes import c_char, c_long, c_ulong
from ctypes.util import find_library
import logging
from .exceptions import ProdaNGOracleException, ProdaNGFunctionalException, ProdaNGException

import platform
from _ctypes import byref
if platform.system() == 'Windows':
    from ctypes import windll as cdll
else:
    from ctypes import cdll


logger = logging.getLogger(__name__)

# regexp for checking if an ipv4 address is valid.
ipv4 = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


class ADict(dict):
    """
    Accessing dict keys like an attribute.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

from .types import errors

class ProdaNGLibrary(object):
    """
    ProdaNG loader and encapsulator. We make this a singleton to make
    sure the library is loaded only once.
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._instance.lib_location = None
            cls._instance.cdll = None
        return cls._instance

    def __init__(self, lib_location=None):
        if self.cdll:
            return
        self.lib_location = lib_location or self.lib_location or find_library('prodllng')
        if not self.lib_location:
            msg = "can't find prodllng library. If installed, try running ldconfig"
            raise ProdaNGException(msg)
        self.cdll = cdll.LoadLibrary(self.lib_location)


def load_library(lib_location=None):
    """
    :returns: a ctypes cdll object with the prodllng shared library loaded.
    """
    return ProdaNGLibrary(lib_location).cdll


def check_error(code, context="client"):
    """
    check if the error code is set. If so, a Python log message is generated
    and an error is raised.
    In case code is 0 - no error is returned
    """
    error_str = ""
    if code is not None:
        if code in errors:
            error_str = errors[code]
    if code == 0:
        logger.debug("Error code: {code}, Error String: {error_str}, Context: {context}".format(code=code, context=context, error_str=error_str))
    elif code < 0:
        oracle_error = str(error_text(code, context))
        error_str = " " + oracle_error
        logger.error("Error code: {code}, Error String: {error_str}, Context: {context}".format(code=code, context=context, error_str=error_str))
        raise ProdaNGOracleException(code, error_str, oracle_error, context)
    elif code > 0:
        logger.error("Error code: {code}, Error String: {error_str}, Context: {context}".format(code=code, context=context, error_str=error_str))
        raise ProdaNGFunctionalException(code, error_str, context)
    

def error_text(error, context="client"):
    """Returns a textual explanation of a given error number

    :param error: an error integer
    :param context: function name that raised error
    :returns: the error string
    """
    logger.debug("reading error text for code: {code}".format(code=error))
    len_ = 1024
    text_type = c_char * len_
    text = text_type()
    library = load_library()
    library.GetLastErrorMsg(error, byref(text), len_)
    return text.value
