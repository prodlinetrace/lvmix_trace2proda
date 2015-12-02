"""
Python equivalent for prodang specific types.
"""
import ctypes
from ctypes import Structure
from .common import ADict

# define some constants
PRODANGDLL_CDBID_SIZE =              16
PRODANGDLL_ISOCODE_SIZE =            34
PRODANGDLL_LANGUAGEDATA_NAME_SIZE =  66
PRODANGDLL_DESCRIPTION_SIZE =       514
PRODANGDLL_MIMETYPE_SIZE =          130
PRODANGDLL_UNITNAME_SIZE =           12
PRODANGDLL_MDREASON_SIZE =          514
PRODANGDLL_MDUSER_SIZE =             22
PRODANGDLL_SYSTEM_NAME_SIZE =        52
PRODANGDLL_PRODUCTNAME_SIZE =        52
PRODANGDLL_WABCONUMBER_SIZE =        12
PRODANGDLL_FILENAME_SIZE =          258
PRODANGDLL_TRANSFER_SIZE =            2
PRODANGDLL_VALUETEXT_SIZE =         258
PRODANGDLL_SERIALNUMBER_SIZE =       32
PRODANGDLL_SERIALNUMBER_SIZE_LSN = 1002
PRODANGDLL_COMMENT_SIZE =           258
PRODANGDLL_MDTIME_SIZE =             24
PRODANGDLL_CRTIME_SIZE =             24
PRODANGDLL_STARTTIME_SIZE =          24
PRODANGDLL_ENDTIME_SIZE =            24
GETTESTSTEPS_ORDERBY_TEST_SEQUENCE = 0  # used for function GetTestSteps_orderby
GETTESTSTEPS_ORDERBY_TEST_ORDER =    1  # used for function GetTestSteps_orderby


# define some basic types
ProdaNGObject = ctypes.c_void_p
dbHandle = ctypes.c_int32
RetVal = ctypes.c_int32
idbID = ctypes.c_int32
cdbID = ctypes.create_string_buffer(PRODANGDLL_CDBID_SIZE)  


# connection errors:
db_connection_errors = {
    -1017: "Oracle error: ORA-1017 invalid username/password; logon denied (suggestion: check db_user or db_pass)",
    -12154: "Oracle error: ORA-12154 TNS: could not resolve the connect identifier specified (suggestion: check db_name, file: tnsnames.ora, file: sqlnet.ora, check ping to Oracle server)",
    -12170: "Oracle error: ORA-12170 TNS:Connect timeout occurred",
    -12541: "Oracle error: ORA-12541 TNS:no listener (host exists but is there Oracle DB? Is listener working on port defined in tnsnames.ora? suggestion: check db_name, file: tnsnames.ora)",
    -12560: "Oracle error: ORA-12560 TNS:protocol adapter error",
}

# define some structures
class LanguageData(Structure):
    __fields__ = [  ("id", idbID), 
                    ("isoCode", ctypes.create_string_buffer(PRODANGDLL_ISOCODE_SIZE)),
                    ("name", ctypes.create_string_buffer(PRODANGDLL_LANGUAGEDATA_NAME_SIZE))
                ]
 
LanguageDataPtr = ctypes.POINTER(LanguageData)
 
 
class OpaqueData(Structure):
    __fields__ = [  ("id", cdbID), 
                    ("mimeTypeId", idbID),
                    ("binLength", ctypes.c_int),
                    ("binary", ctypes.c_void_p),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE))
                ]

OpaqueDataPtr = ctypes.POINTER(OpaqueData)


class MimeType(Structure):
    __fields__ = [  ("id", idbID), 
                    ("mimeType", ctypes.create_string_buffer(PRODANGDLL_MIMETYPE_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE))
                ]

MimeTypePtr = ctypes.POINTER(MimeType)


class UnitData(Structure):
    __fields__ = [  ("id", idbID), 
                    ("unitName", ctypes.create_string_buffer(PRODANGDLL_UNITNAME_SIZE)),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE))
                ]

UnitDataPtr = ctypes.POINTER(UnitData)


class Identification(Structure):
    __fields__ = [  ("id", idbID),
                    ("processId", idbID),
                    ("systemId", idbID),
                    ("processStepId", idbID),
                    ("wabcoPartId", idbID) 
                ]   

IdentificationPtr = ctypes.POINTER(Identification)


class System(Structure):
    __fields__ = [  ("id", idbID), 
                    ("name", ctypes.create_string_buffer(PRODANGDLL_SYSTEM_NAME_SIZE))
                ]
 
SystemPtr = ctypes.POINTER(System)
 
 
class WabcoPart(Structure):
    __fields__ = [  ("id", idbID),
                    ("workCenterId", idbID),
                    ("contentId", idbID),
                    ("previewId", idbID),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("productName", ctypes.create_string_buffer(PRODANGDLL_PRODUCTNAME_SIZE)),
                    ("wabcoNumber", ctypes.create_string_buffer(PRODANGDLL_WABCONUMBER_SIZE)),
                ]

WabcoPartPtr = ctypes.POINTER(WabcoPart)


class Process(Structure):
    __fields__ = [  ("id", idbID),
                    ("productionLineId", idbID),
                    ("releaseId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

ProcessPtr = ctypes.POINTER(Process)    


class ProcessStep(Structure):
    __fields__ = [  ("id", idbID),
                    ("processId", idbID),
                    ("systemId", idbID),
                    ("releaseId", idbID),
                    ("processSequence", ctypes.c_int),
                    ("limitYellow", ctypes.c_double),
                    ("limitRed", ctypes.c_double),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("filename", ctypes.create_string_buffer(PRODANGDLL_FILENAME_SIZE)),
                    ("transfer", ctypes.create_string_buffer(PRODANGDLL_TRANSFER_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

ProcessStepPtr = ctypes.POINTER(ProcessStep)


class ProcessStepParam(Structure):
    __fields__ = [  ("id", idbID),
                    ("processStepId", idbID),
                    ("unitId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("value", ctypes.c_double),
                    ("valueText", ctypes.create_string_buffer(PRODANGDLL_VALUETEXT_SIZE)),                    
                    ("paramSequence", ctypes.c_int),
                    ("history", ctypes.c_int),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

ProcessStepParamPtr = ctypes.POINTER(ProcessStepParam)


class TestStep(Structure):
    __fields__ = [  ("id", idbID),
                    ("processStepId", idbID),
                    ("testSequence", ctypes.c_int),
                    ("testOrder", ctypes.c_int),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

TestStepPtr = ctypes.POINTER(TestStep)


class TestStepParam(Structure):
    __fields__ = [  ("id", idbID),
                    ("testStepId", idbID),
                    ("unitId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("value", ctypes.c_double),
                    ("valueText", ctypes.create_string_buffer(PRODANGDLL_VALUETEXT_SIZE)),                    
                    ("paramSequence", ctypes.c_int),
                    ("history", ctypes.c_int),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

TestStepParamPtr = ctypes.POINTER(TestStepParam)


class TestValue(Structure):
    __fields__ = [  ("id", idbID),
                    ("testStepId", idbID),
                    ("releaseId", idbID),
                    ("unitId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("maximum", ctypes.c_double),
                    ("minimum", ctypes.c_double),
                    ("valueText", ctypes.create_string_buffer(PRODANGDLL_VALUETEXT_SIZE)),                    
                    ("testValueSequence", ctypes.c_int),
                    ("history", ctypes.c_int),
                    ("mdReason", ctypes.create_string_buffer(PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", ctypes.create_string_buffer(PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

TestValuePtr = ctypes.POINTER(TestValue)


class Product(Structure):
    __fields__ = [  ("id", cdbID),
                    ("wabcoPartId", idbID),
                    ("serialNumber", ctypes.create_string_buffer(PRODANGDLL_SERIALNUMBER_SIZE)),
                    ("comment", ctypes.create_string_buffer(PRODANGDLL_COMMENT_SIZE)),
                    ("individual", ctypes.c_int),
                    ("crProcessStepId", idbID),
                    ("mdProcessStepId", idbID),
                    ("crTime", ctypes.create_string_buffer(PRODANGDLL_CRTIME_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                ]

ProductPtr = ctypes.POINTER(Product)


class Product_lsn(Structure):
    __fields__ = [  ("id", cdbID),
                    ("wabcoPartId", idbID),
                    ("serialNumber", ctypes.create_string_buffer(PRODANGDLL_SERIALNUMBER_SIZE_LSN)),
                    ("comment", ctypes.create_string_buffer(PRODANGDLL_COMMENT_SIZE)),
                    ("individual", ctypes.c_int),
                    ("crProcessStepId", idbID),
                    ("mdProcessStepId", idbID),
                    ("crTime", ctypes.create_string_buffer(PRODANGDLL_CRTIME_SIZE)),
                    ("mdTime", ctypes.create_string_buffer(PRODANGDLL_MDTIME_SIZE)),
                ]

Product_lsnPtr = ctypes.POINTER(Product_lsn)


class ProcessResult(Structure):
    __fields__ = [  ("id", cdbID),
                    ("productId", cdbID),
                    ("processId", idbID),
                    ("statusId", idbID),
                    ("startTime", ctypes.create_string_buffer(PRODANGDLL_STARTTIME_SIZE)),
                    ("endTime", ctypes.create_string_buffer(PRODANGDLL_ENDTIME_SIZE)),
                ]

ProcessResultPtr = ctypes.POINTER(ProcessResult)


class ProcessStepResult(Structure):
    __fields__ = [  ("id", cdbID),
                    ("processResultId", cdbID),
                    ("processStepId", idbID),
                    ("statusId", idbID),
                    ("operatorId", idbID),
                    ("startTime", ctypes.create_string_buffer(PRODANGDLL_STARTTIME_SIZE)),
                    ("endTime", ctypes.create_string_buffer(PRODANGDLL_ENDTIME_SIZE)),
                ]

ProcessStepResultPtr = ctypes.POINTER(ProcessStepResult)


class TestStepResult(Structure):
    __fields__ = [  ("id", cdbID),
                    ("processStepResultId", cdbID),
                    ("testStepId", idbID),
                    ("statusId", idbID),
                ]

TestStepResultPtr = ctypes.POINTER(TestStepResult)


class TestValueResult(Structure):
    __fields__ = [  ("id", cdbID),
                    ("testStepResultId", cdbID),
                    ("testValueId", idbID),
                    ("result", ctypes.c_double),
                    ("statusId", idbID),
                    ("contentId", cdbID),
                ]

TestValueResultPtr = ctypes.POINTER(TestValueResult)


class ProductionLine(Structure):
    __fields__ = [  ("id", idbID),
                    ("description", ctypes.create_string_buffer(PRODANGDLL_DESCRIPTION_SIZE)),
                ]

ProductionLinePtr = ctypes.POINTER(ProductionLine)


class Product_Component(Structure):
    __fields__ = [  ("product", Product_lsnPtr),
                    ("component", Product_lsnPtr),
                    ("processStepResult", ProcessStepResultPtr),
                    ("qty", ctypes.c_int),
                    ("level", ctypes.c_int),
                ]

Product_ComponentPtr = ctypes.POINTER(Product_Component)


class Product_Component_wnr_snr(Structure):
    __fields__ = [  ("product_wabcoNumber", ctypes.create_string_buffer(PRODANGDLL_WABCONUMBER_SIZE)),
                    ("product_serialNumber", ctypes.create_string_buffer(PRODANGDLL_SERIALNUMBER_SIZE_LSN)),
                    ("component_wabcoNumber", ctypes.create_string_buffer(PRODANGDLL_WABCONUMBER_SIZE)),
                    ("component_serialNumber", ctypes.create_string_buffer(PRODANGDLL_SERIALNUMBER_SIZE_LSN)),
                    ("processStepResultId", cdbID),
                    ("qty", ctypes.c_int),
                    ("level", ctypes.c_int),
                ]

Product_Component_wnr_snrPtr = ctypes.POINTER(Product_Component_wnr_snr)