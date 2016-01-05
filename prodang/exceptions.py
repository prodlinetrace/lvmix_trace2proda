class ProdaNGException(Exception):
    """
    A ProdaNG specific exception.
    """
    pass

class ProdaNGDBConnectionError(ProdaNGException):
    """
    A ProdaNG specific exception.
    """
    pass

class ProdaNGOracleException(ProdaNGException):
    """
    A ProdaNG Oracle specific exception.
    """
    pass

class ProdaNGFunctionalException(ProdaNGException):
    """
    A ProdaNG functional exception.
    """
    pass
