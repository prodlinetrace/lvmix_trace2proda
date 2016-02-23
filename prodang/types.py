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
cdbID = (ctypes.c_char * PRODANGDLL_CDBID_SIZE)  


# connection errors:
db_connection_errors = {
    -1017:  "Oracle error: ORA-1017 invalid username/password; logon denied (suggestion: check db_user or db_pass)",
    -1858:  "Oracle error: ORA-1858 a non-numeric character was found where a numeric was expected",
    -12154: "Oracle error: ORA-12154 TNS: could not resolve the connect identifier specified (suggestion: check db_name, file: tnsnames.ora, file: sqlnet.ora, check ping to Oracle server)",
    -12170: "Oracle error: ORA-12170 TNS:Connect timeout occurred",
    -12541: "Oracle error: ORA-12541 TNS:no listener (host exists but is there Oracle DB? Is listener working on port defined in tnsnames.ora? suggestion: check db_name, file: tnsnames.ora)",
    -12560: "Oracle error: ORA-12560 TNS:protocol adapter error",
}

functional_errors = {
    0:      "OK",
    1:      "Functional error: Context is no longer available. In this case numContexts in InitProDll() should be increased.",
    6:      "Functional error: (ERROR_INVALID_HANDLE) in case of an invalid handle",
    7:      "Functional error: WabcoNumber not found in wabcopart table",
    8:      "Functional error: newWabcoNumber not found in wabcopart table",
    9:      "Functional error: SerialNumber, WabcoNumber not found in product table with individual=1",
    232:    "Functional error: (ERROR_NO_DATA) in case of an invalid data", 
    234:    "Functional error: (ERROR_MORE_DATA) in case that the MAXBLOBSIZE is exceeded.",
    1403:   "Functional error: Record does not exist",
}

#errors = db_connection_errors + functional_errors
errors = db_connection_errors.copy()
errors.update(functional_errors)

# define some structures
class LanguageData(Structure):
    _fields_ = [    ("id", idbID), 
                    ("isoCode", (ctypes.c_char * PRODANGDLL_ISOCODE_SIZE)),
                    ("name", (ctypes.c_char * PRODANGDLL_LANGUAGEDATA_NAME_SIZE)),
    ]
    
    __repr__ = "<{t} Id: {id}>, Name: {name}".format(t=type, id="id", name="name")
 
LanguageDataPtr = ctypes.POINTER(LanguageData)
 
 
class OpaqueData(Structure):
    _fields_ = [    ("id", cdbID), 
                    ("mimeTypeId", idbID),
                    ("binLength", ctypes.c_int),
                    ("binary", ctypes.c_void_p),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

OpaqueDataPtr = ctypes.POINTER(OpaqueData)


class MimeType(Structure):
    _fields_ = [    ("id", idbID), 
                    ("mimeType", (ctypes.c_char * PRODANGDLL_MIMETYPE_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

MimeTypePtr = ctypes.POINTER(MimeType)


class UnitData(Structure):
    _fields_ = [    ("id", idbID), 
                    ("unitName", (ctypes.c_char * PRODANGDLL_UNITNAME_SIZE)),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

UnitDataPtr = ctypes.POINTER(UnitData)


class Identification(Structure):
    _fields_ = [    
                    ("processId", idbID),
                    ("systemId", idbID),
                    ("processStepId", idbID),
                    ("wabcoPartId", idbID), 
    ]

IdentificationPtr = ctypes.POINTER(Identification)


class System(Structure):
    _fields_ = [    ("id", idbID), 
                    ("name", (ctypes.c_char * PRODANGDLL_SYSTEM_NAME_SIZE)),
    ]
 
SystemPtr = ctypes.POINTER(System)
 
 
class WabcoPart(Structure):
    _fields_ = [    ("id", idbID),
                    ("workCenterId", idbID),
                    ("contentId", idbID),
                    ("previewId", idbID),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("productName", (ctypes.c_char * PRODANGDLL_PRODUCTNAME_SIZE)),
                    ("wabcoNumber", (ctypes.c_char * PRODANGDLL_WABCONUMBER_SIZE)),
    ]

WabcoPartPtr = ctypes.POINTER(WabcoPart)


class Process(Structure):
    _fields_ = [    ("id", idbID),
                    ("productionLineId", idbID),
                    ("releaseId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

ProcessPtr = ctypes.POINTER(Process)    


class ProcessStep(Structure):
    _fields_ = [    ("id", idbID),
                    ("processId", idbID),
                    ("systemId", idbID),
                    ("releaseId", idbID),
                    ("processSequence", ctypes.c_int),
                    ("limitYellow", ctypes.c_double),
                    ("limitRed", ctypes.c_double),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("filename", (ctypes.c_char * PRODANGDLL_FILENAME_SIZE)),
                    ("transfer", (ctypes.c_char * PRODANGDLL_TRANSFER_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

ProcessStepPtr = ctypes.POINTER(ProcessStep)


class ProcessStepParam(Structure):
    _fields_ = [    ("id", idbID),
                    ("processStepId", idbID),
                    ("unitId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("value", ctypes.c_double),
                    ("valueText", (ctypes.c_char * PRODANGDLL_VALUETEXT_SIZE)),                    
                    ("paramSequence", ctypes.c_int),
                    ("history", ctypes.c_int),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

ProcessStepParamPtr = ctypes.POINTER(ProcessStepParam)


class TestStep(Structure):
    _fields_ = [    ("id", idbID),
                    ("processStepId", idbID),
                    ("testSequence", ctypes.c_int),
                    ("testOrder", ctypes.c_int),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

TestStepPtr = ctypes.POINTER(TestStep)


class TestStepParam(Structure):
    _fields_ = [    ("id", idbID),
                    ("testStepId", idbID),
                    ("unitId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("value", ctypes.c_double),
                    ("valueText", (ctypes.c_char * PRODANGDLL_VALUETEXT_SIZE)),                    
                    ("paramSequence", ctypes.c_int),
                    ("history", ctypes.c_int),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

TestStepParamPtr = ctypes.POINTER(TestStepParam)


class TestValue(Structure):
    _fields_ = [    ("id", idbID),
                    ("testStepId", idbID),
                    ("releaseId", idbID),
                    ("unitId", idbID),
                    ("contentId", cdbID),
                    ("previewId", cdbID),
                    ("maximum", ctypes.c_double),
                    ("minimum", ctypes.c_double),
                    ("valueText", (ctypes.c_char * PRODANGDLL_VALUETEXT_SIZE)),                    
                    ("testValueSequence", ctypes.c_int),
                    ("history", ctypes.c_int),
                    ("mdReason", (ctypes.c_char * PRODANGDLL_MDREASON_SIZE)),
                    ("mdUser", (ctypes.c_char * PRODANGDLL_MDUSER_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

TestValuePtr = ctypes.POINTER(TestValue)


class Product(Structure):
    _fields_ = [    ("id", cdbID),
                    ("wabcoPartId", idbID),
                    ("serialNumber", (ctypes.c_char * PRODANGDLL_SERIALNUMBER_SIZE)),
                    ("comment", (ctypes.c_char * PRODANGDLL_COMMENT_SIZE)),
                    ("individual", ctypes.c_int),
                    ("crProcessStepId", idbID),
                    ("mdProcessStepId", idbID),
                    ("crTime", (ctypes.c_char * PRODANGDLL_CRTIME_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
    ]

ProductPtr = ctypes.POINTER(Product)


class Product_lsn(Structure):
    _fields_ = [    ("id", cdbID),
                    ("wabcoPartId", idbID),
                    ("serialNumber", (ctypes.c_char * PRODANGDLL_SERIALNUMBER_SIZE_LSN)),
                    ("comment", (ctypes.c_char * PRODANGDLL_COMMENT_SIZE)),
                    ("individual", ctypes.c_int),
                    ("crProcessStepId", idbID),
                    ("mdProcessStepId", idbID),
                    ("crTime", (ctypes.c_char * PRODANGDLL_CRTIME_SIZE)),
                    ("mdTime", (ctypes.c_char * PRODANGDLL_MDTIME_SIZE)),
    ]

Product_lsnPtr = ctypes.POINTER(Product_lsn)


class ProcessResult(Structure):
    _fields_ = [    ("id", cdbID),
                    ("productId", cdbID),
                    ("processId", idbID),
                    ("statusId", idbID),
                    ("startTime", (ctypes.c_char * PRODANGDLL_STARTTIME_SIZE)),
                    ("endTime", (ctypes.c_char * PRODANGDLL_ENDTIME_SIZE)),
    ]

ProcessResultPtr = ctypes.POINTER(ProcessResult)


class ProcessStepResult(Structure):
    _fields_ = [    ("id", cdbID),
                    ("processResultId", cdbID),
                    ("processStepId", idbID),
                    ("statusId", idbID),
                    ("operatorId", idbID),
                    ("startTime", (ctypes.c_char * PRODANGDLL_STARTTIME_SIZE)),
                    ("endTime", (ctypes.c_char * PRODANGDLL_ENDTIME_SIZE)),
    ]

ProcessStepResultPtr = ctypes.POINTER(ProcessStepResult)


class TestStepResult(Structure):
    _fields_ = [    ("id", cdbID),
                    ("processStepResultId", cdbID),
                    ("testStepId", idbID),
                    ("statusId", idbID),
    ]

TestStepResultPtr = ctypes.POINTER(TestStepResult)


class TestValueResult(Structure):
    _fields_ = [    ("id", cdbID),
                    ("testStepResultId", cdbID),
                    ("testValueId", idbID),
                    ("result", ctypes.c_double),
                    ("statusId", idbID),
                    ("contentId", cdbID),
    ]

TestValueResultPtr = ctypes.POINTER(TestValueResult)


class ProductionLine(Structure):
    _fields_ = [    ("id", idbID),
                    ("description", (ctypes.c_char * PRODANGDLL_DESCRIPTION_SIZE)),
    ]

ProductionLinePtr = ctypes.POINTER(ProductionLine)


class Product_Component(Structure):
    _fields_ = [    ("product", Product_lsnPtr),
                    ("component", Product_lsnPtr),
                    ("processStepResult", ProcessStepResultPtr),
                    ("qty", ctypes.c_int),
                    ("level", ctypes.c_int),
    ]

Product_ComponentPtr = ctypes.POINTER(Product_Component)


class Product_Component_wnr_snr(Structure):
    _fields_ = [    ("product_wabcoNumber", (ctypes.c_char * PRODANGDLL_WABCONUMBER_SIZE)),
                    ("product_serialNumber", (ctypes.c_char * PRODANGDLL_SERIALNUMBER_SIZE_LSN)),
                    ("component_wabcoNumber", (ctypes.c_char * PRODANGDLL_WABCONUMBER_SIZE)),
                    ("component_serialNumber", (ctypes.c_char * PRODANGDLL_SERIALNUMBER_SIZE_LSN)),
                    ("processStepResultId", cdbID),
                    ("qty", ctypes.c_int),
                    ("level", ctypes.c_int),
    ]

Product_Component_wnr_snrPtr = ctypes.POINTER(Product_Component_wnr_snr)