"""
prodang client used for connection to a Wabco's Proda database.
"""
import re
#import ctypes
#from ctypes import c_int, c_char_p, byref, sizeof, c_uint16, c_int32, c_byte, c_void_p, c_char
from ctypes import *
import logging
from datetime import datetime

import prodang
from prodang.common import check_error, load_library, ipv4
from prodang.exceptions import ProdaNGException, ProdaNGDBConnectionError
from prodang.types import *

logger = logging.getLogger(__name__)


def error_wrap(func):
    """Parses a prodang error code returned the decorated function."""
    def f(*args, **kw):
        items = func(*args, **kw)
        code = items.pop(0)  # read and remove first returned argument 
        check_error(code, context=func.__name__)
        return items[0]
    return f


class Client(object):
    """
    A prodang client
    """
    def __init__(self, lib_location=None):
        self.library = load_library(lib_location)
        self.pointer = False
        self.db_handle = None
        self.result = 0
        self.init_pro_dll()

    def db_connect(self, user, password, database):
        """
        create a ProdaNG db connection.
        """
        logger.debug("creating prodang database connection")
        #self.library.Cli_Create.restype = c_void_p
        #self.pointer = ProdaNGObject(self.library.InitProDll())
        self.user = user
        self.password = password
        self.database = database
        self.login(user, password, database)
        
    def db_disconnect(self):
        self.logout()
        self.exit_pro_dll()

    def init_pro_dll(self):
        result = (self.library.InitProDll(c_int(1)))
        if result == 0:
            logger.debug("InitProDll successful".format())
        else:
            logger.error("InitProDll failed. Return code is: {code}".format(code=result))
        return result

    def exit_pro_dll(self):
        """
        destroy a client.
        """
        logger.debug("destroying prodang client")
        return self.library.ExitProDll()

    @error_wrap
    def login(self, user, password, database):
        """
        This function offers the logon to an Oracle database and can be called in every Thread. In case that the DLL is running in a Shared Context, an existing connection to ORACLE will be terminated first and afterwards reconstructed! In the other case the connection is constructed and a new Handle is created. During the Login phase it is being tried repeatedly to establish the connection to the database. The number of retries is 5, each with 5 seconds standby time between the efforts. If a connection is not possible, this function returns afterwards with the responding Oracle error code.
        Returncodes:
            0        no error
            < 0    ORACLE error code. Because no valid handle was created, the function GetLastErrorMsg() cannot be used.
            1    Context is no longer available. In this case numContexts in InitProDll() should be increased.

        :param user - User account in the database
        :param password - Password of the database user account 
        :param database - Service name or SID of the used database
        :returns handle 
        """
        
        operation = "logging in to database"
        logger.debug("Operation: {operation}, as user/password@database: {user}/{password}@{database}".format(operation=operation, user=user, password=password, database=database))

        handle = (dbHandle)()
        result = int(self.library.Login(user, password, database, byref(handle)))

        log_msg = "Result: {result}, Operation: {operation},, Func_name: {name}. Handle: {handle}, user: {user}, password: {password}, database: {database}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, user=user, password=password, database=database)
        if result == 0:
            logger.info("DB login successful {name}".format(name=__name__))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))
        
        # set the db_handle
        self.db_handle = handle.value
        
        return [result, self.db_handle]

    @error_wrap
    def logout(self):
        """
        The function allows the Logoff from the Oracle database. A return value passes back the result of the termination of the connection. It can be called in every thread. The connection to ORACLE is being terminated for the context of the specified Handle and all resources of the handle will be released. If it is being worked with a Shared Context, no thread can access ORACLE afterwards!
        Returncodes:
            0        no Error
            < 0    ORACLE Error code. Because the Handle is invalid when returning from the function, the function GetLastErrorMsg() cannot be used.
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        :param handle 
        :returns retval 
        """
        
        operation = "logging out from database"
        logger.debug("{operation}. Handle: {handle}".format(operation=operation, handle=self.db_handle))

        result = int(self.library.Logout(self.db_handle))

        if result == 0:
            logger.info("DB logout successful {name}".format(name=__name__))
        else:
            logger.error("DB logout failed in {name}. Error Code: {code}".format(name=__name__, code=result))
                    
        return [result, None]

    @error_wrap
    def set_db_id(self, dbId):
        """
        This function overwrites the standard respectively preference value of the DBID for this session until a Logout().

        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            dbId is an Integer, which indicates the DBID, which should be used at the creation of new rows in the database. A further use of DBID does not take place in the DLL.


        Returncodes:
            0        No error
            < 0    ORACLE error code 
            6 (ERROR_INVALID_HANDLE) in case of an invalid handle
        """
        
        operation = "Setting the Database ID (DBID)"
        logger.debug("{operation}. Handle: {handle}, dbId: {dbId}".format(operation=operation, handle=self.db_handle, dbId=dbId))
        result = int(self.library.SetDBId(self.db_handle, dbId))
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, dbId: {dbId}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, dbId=dbId)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))
                    
        return [result, None]
        

    @error_wrap
    def set_preference(self, key, value):
        """
        This function overwrites the standard value for the preference named in key for this session until a Logout().

        Parameter:
            handle ist ein Integer, den die Funktion Login() bei Erzeugung einer neue Verbindung zuruckgibt.
            key  is the name of the preference to set. Actual the following preferences are supported:
                RETRYCOUNT            
                RETRYWAIT
                RETRYISRECONNECT
                IGNORERELEASEID

        According to the preference name the integer passed in value will be used as
            Number of retries in case of a database Retry/Reconnect
            Number of seconds to wait between two retries
            A value not equal 0 in case a Retry always leads to Reconnect.
            A value not equal 0 in case Release Id's should be ignored while fetching from process description tables. This is used in process test environments only!

        Returncodes:
            0        No error
            6        (ERROR_INVALID_HANDLE) in case of an invalid handle
            232      (ERROR_NO_DATA) in case of an invalid preference
        """
        
        operation = "Setting preference"
        logger.debug("{operation} {name}. Handle: {handle}, key: {key}, value: {value}".format(operation=operation, name=__name__, handle=self.db_handle, key=key, value=value))
        result = int(self.library.SetPreference(self.db_handle, key, value))
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, key: {key}, value: {value}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, key=key, value=value)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))
                    
        return [result, None]

    def get_last_error_msg(self):
        """
        This function returns the text of the last ORACLE error for a defined context. This function can only be used with a valid Handle.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
        Return Value:
            Last ORACLE error message
            In case that a handle is invalid, an empty string is returned.
        """
        
        operation = "Getting last Oracle error message"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        buf = time_buf = (c_char * 1024)()
        result = self.library.GetLastErrorMsg(self.db_handle, byref(buf))
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}".format(operation=operation, result=result, name=__name__, handle=self.db_handle)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                
        return buf.value


    @error_wrap
    def get_database_time(self):
        """
        This function passes back the current system time of the database.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            timeBuf is a Character Array in which the time given back in the format DD.MM.YYYY HH24:MI:SS when the Returncode is 0.
        
        Gets datetime structure from DB and transforms it to python's time.struct_time
        """
        
        operation = "Getting Database Time"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        time_buf = (c_char * 24)()
        result = self.library.GetDatabaseTime(self.db_handle, byref(time_buf))
        #print time_buf.value
        struct_datetime = datetime.strptime(time_buf.value.strip(), "%d.%m.%Y %H:%M:%S")
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, datetime: {struct_datetime}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, struct_datetime=struct_datetime)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, struct_datetime]


    @error_wrap
    def get_languages(self):
        """
        This function returns all available languages.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            Languages is a pointer, in which the languages are returned as an array of pointers on language data structures, when the returncode is 0.
            typedef struct LanguageData {
                idbID    id;            // Id of Record
                char    isoCode[34];    // Iso Code (en,de,)
                char    name[66];        // Descriptional name (English)
            } * LanguageDataPtr;
            
            countPtr is a pointer on an Integer in which the number of records is returned in *languages, if the returncode 0. 
            
        Returncodes:
            0    No error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
            
        An example, that is representative for all functions that work with arrays:
        
        LanguageDataPtr    *langArray;
        int count;
        RetVal i = GetLanguages(handle, &langArray, &count);
        // Check errors and counts [omitted]
        LanguageDataPtr lang1 = langArray[0]; // Access first record
        char *iso = lang1->isoCode;    // Access isoCode in first language
        FreeStructArray((void **)langArray); // Free the array after 
        
        
        @return languages - hash of languages   
        """
        operation = "Getting All Languages"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        languageDataPtr = pointer(LanguageDataPtr())
        result = self.library.GetLanguages(self.db_handle, byref(languageDataPtr), byref(countPtr))
        lang_count = countPtr.value
        languages = {}
        for item in languageDataPtr[:lang_count]:
            if item.contents is None:
                break
            lang = {
                    'id': item.contents.id, 
                    'isoCode': item.contents.isoCode,
                    'name': item.contents.name,
            }
            languages[item.contents.id] = lang

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, lang_count: {lang_count}, languages: {languages}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, lang_count=lang_count, languages=languages)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, languages]

    @error_wrap
    def set_language(self, languageId):
        """
        This function sets the wanted language for this session and overwrites the default value respective Preference LANGUAGEID with it.
        In subsequent functions, that delivers or writes language-dependent data, the id specifies language that should be used. If a description is not existent in the desired language, the description is taken from the language 0 (English).
        If a language-dependent description is inserted or changed, it is being marked with the currently set language. Additionally this description is deposited for language 0, in case that the description does not exist and the current language is not 0.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            languageId is the Id of one language, which is returned from GetLanguages().
        
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6 (ERROR_INVALID_HANDLE) in case of an invalid handle
            232    (ERROR_NO_DATA) in case of an invalid Id.
        """
        
        operation = "Setting Language"
        logger.debug("{operation}. Handle: {handle}, languageId: {languageId}".format(operation=operation, handle=self.db_handle, languageId=languageId))
        result = int(self.library.SetLanguage(self.db_handle, languageId))
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, languageId: {languageId}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, languageId=languageId)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))
                    
        return [result, None]

    @error_wrap
    def get_units(self):
        """
        RetVal GetUnits ( dbHandle handle, UnitDataPtr **units, int *countPtr )
        This function returns all available units, sorted by their names.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            units is a pointer, in which the units are returned as an array of pointers on unit data structures , if the returncode is 0.
            typedef struct UnitData {
                idbID    id;            // Id of Record
                char    unitName[12];    // Name of unit
                char    mdReason[514];    // Reason of last change
                char    mdUser[22];        // Last changed by user
                char    mdTime[24];        // Date of last change
                char    description[514];    // Translated description
            } * UnitDataPtr;
        
            countPtr is a pointer on an Integer in which the number of records in *units is returned, if the returncode is 0.
        
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        
        @return units - hash of all units   
        """
        operation = "Getting All units"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        unitDataPtr = pointer(UnitDataPtr())
        result = self.library.GetUnits(self.db_handle, byref(unitDataPtr), byref(countPtr))
        count = countPtr.value
        units = {}
        for item in unitDataPtr[:count]:
            if item.contents is None:
                break
            unit = {
                    'id': item.contents.id, 
                    'unitName': item.contents.unitName,
                    'mdReason': item.contents.mdReason,
                    'mdUser': item.contents.mdUser,
                    'mdTime': item.contents.mdTime,
                    'description': item.contents.description,
            }
            units[item.contents.id] = unit

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, units: {units}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, units=units)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, units]

    @error_wrap
    def get_opaque_data(self, opaque_id):
        """
        RetVal GetOpaqueData    ( dbHandle handle, cdbID opaqueId, OpaqueDataPtr opaqueData )
        This function returns an OpaqueData structure for a defined id.
        Please note: The field binary is being allocated in the memory by the DLL and must be released by the user of the DLL.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            opaqueId is the id of the record to be read.
            opaqueData is a pointer on an OpaqueData structure, which is filled, if the returncode is 0. The structure must be defined in the calling program.
            typedef struct OpaqueData {
                cdbID    id;            // Id of Record
                idbID    mimeTypeId;        // Id of associated mime type
                int      binLength;        // Length of binary data
                void     *binary;        // Pointer to binary data
                char    description[514];    // Translated description
            } *OpaqueDataPtr;
        
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6 (ERROR_INVALID_HANDLE) in case of an invalid handle
            1403    Record does not exist
        
        
        @return opaque_data - hash of opaque_data   
        """
        operation = "Getting opqaue data"
        logger.debug("{operation} {name}. Handle: {handle}, opaque_id: {opaque_id}".format(operation=operation, name=__name__, handle=self.db_handle, opaque_id=opaque_id))
        
        opaqueDataPtr = pointer(OpaqueDataPtr())
        result = self.library.GetOpaqueData(self.db_handle, opaque_id, byref(opaqueDataPtr))
        for item in opaqueDataPtr:
            if item.contents is None:
                break
            opaque_data = {
                    'id': item.contents.id, 
                    'mimeTypeId': item.contents.mimeTypeId,
                    'binLength': item.contents.binLength,
                    'binary': item.contents.binary,
                    'description': item.contents.description,
            }
            #opaque_data[item.contents.id] = lang

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, opaque_id: {opaque_id}, opaque_data: {opaque_data}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, opaque_id=opaque_id, opaque_data=opaque_data)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, opaque_data]


    def get_opaque_data_result(self, opaque_id):
        #TODO: implement
        pass

    def new_opaque_data(self, opaque_data):
        #TODO: implement
        pass

    def new_opaque_data_result(self, opaque_data):
        #TODO: implement
        pass

    def set_opaque_data(self, opaque_data):
        #TODO: implement
        pass

    def set_opaque_data_result(self, opaque_data):
        #TODO: implement
        pass

    def delete_opaque_data(self, opaque_id):
        #TODO: implement
        pass

    def delete_opaque_data_result(self, opaque_id):
        #TODO: implement
        pass

    @error_wrap
    def get_mime_types(self):
        """
        RetVal GetMimeTypes ( dbHandle handle, MimeTypePtr **mimeTypes, int *countPtr )
        
        This function returns all available MIME types. The corresponding id's can be used in the OpaqueData structure.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            mimeTypes is a pointer in which the Mime types are returned as an array of pointers on MimeType structures, if the returncode is 0.
            typedef struct MimeType {
                idbID    id;            // Id of record
                char    mimeType[130];    // Mimetype (image/jpeg)
                char    description[514];    // Translated description
            } *MimeTypePtr;
            countPtr is a pointer on an Integer, which returns the number of records in *mimeTypes, if the returncode is 0.
        
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        
        @return mime_types - hash of mime_types   
        """
        operation = "Getting All MIME types"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        mimeTypePtr = pointer(MimeTypePtr())
        result = self.library.GetMimeTypes(self.db_handle, byref(mimeTypePtr), byref(countPtr))
        count = countPtr.value
        mime_types = {}
        for item in mimeTypePtr[:count]:
            if item.contents is None:
                break
            entry = {
                    'id': item.contents.id, 
                    'mimeType': item.contents.mimeType,
                    'description': item.contents.description,
            }
            mime_types[item.contents.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, mime_types: {mime_types}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, mime_types=mime_types)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, mime_types]


    def update_wabco_number(self):
        #TODO: implement
        pass

    @error_wrap
    def get_systems(self):
        """
        RetVal GetSystems ( dbHandle handle, SystemPtr **systems, int *countPtr )
        
        This function returns all available systems.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            systems is a pointer in which the systems are returned as an array of pointers on system structures, if the returncode is 0.
            typedef struct System {
                idbID    id;            // Id of Record    
                char    name[52];        // Name of system
            } *SystemPtr;
            countPtr is a pointer on an Integer, which returns the number of records in *systems, if the Returncode is 0.
        
        Returncodes:
            0    No Error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        
        @return systems - hash of systems   
        """
        operation = "Getting All Systems"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        systemPtr = pointer(SystemPtr())
        result = self.library.GetSystems(self.db_handle, byref(systemPtr), byref(countPtr))
        count = countPtr.value
        systems = {}
        for item in systemPtr[:count]:
            if item.contents is None:
                break
            entry = {
                    'id': item.contents.id, 
                    'name': item.contents.name,
            }
            systems[item.contents.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, systems: {systems}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, systems=systems)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return systems
        return [result, systems]


    @error_wrap
    def get_system(self, system_id):
        """
        RetVal GetSystem ( dbHandle handle, idbID systemId, SystemPtr system )
        This function returns a system structure for a defined id.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            systemId is the id of the record that should be read.
            system is a pointer on a system structure, which is filled when the Returncode is 0. The structure must be defined in the calling program.
        
        Returncodes:
            0    No error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
            1403    Record not found
        
        @return system - hash of system
        """
        operation = "Getting system"
        logger.debug("{operation} {name}. Handle: {handle}, system_id: {system_id}".format(operation=operation, name=__name__, handle=self.db_handle, system_id=system_id))
        
        system_buf = System()
        result = self.library.GetSystem(self.db_handle, system_id, byref(system_buf))
        system = {
                'id': system_buf.id, 
                'name': system_buf.name,
        }
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, system_id: {system_id}, system: {system}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, system_id=system_id, system=system)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, system]

    def start_idle_time(self):
        #TODO: implement
        pass

    def end_idle_time(self):
        #TODO: implement
        pass

    @error_wrap
    def identify_me(self, system_name, wabco_number, process_sequence, process_id):
        """
        RetVal IdentifyMe    ( dbHandle handle, char *systemName, 
                char *wabcoNumber, int processSequence, 
                idbID processId, IdentificationPtr myIdent )
        This function serves for identifying a system, if for example, the name and the Wabco Number of the tested part, or the process id and the sequential number in a process are known. 
        Attention: This function takes the IGNORERELEASEID preference into account.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            systemName is the name of the system, as it is deposited in the database. If unknown, NULL must be passed.
            wabcoNumber is a known Wabco number in the database. If unknown, NULL must be passed.
            processSequence is the sequential Number in the process. If unknown, 0 must be passed.
            processId is the according process id. If unknown, 0 must be passed.
            
            myIdent is a pointer on an identification structure, if the returncode is 0. The structure must be defined in the calling program. The function tries to identify the system definitely under the aid of the passed parameter, in order to return the resulting id's in MyIdent.
            typedef struct Identification {
                idbID    processId;        // This process
                idbID    systemId;        // This system
                idbID    processStepId;    // The process step id
                idbID    wabcoPartId;    // The Wabco part id 
            }  *IdentificationPtr;.
            The function tries to identify the system from the following combinations of the parameter:
            systemName, 
            processId, 
            systemName and wabcoNumber, 
            processId and processSequence 
            or from all 4 parameter.
            The more parameters are set, the bigger is the chance, that the system can be identified.
        Returncodes:
            0    No error
            < 0    ORACLE Error Code
            6 (ERROR_INVALID_HANDLE) in case of an invalid handle
            232 (ERROR_NO_DATA) in case that the system cannot be identified definitely.
        
        @return identification - hash
        """
        operation = "IdentifyMe"
        logger.debug("{operation} {name}. Handle: {handle}, system_name: {system_name}, wabco_number: {wabco_number}, process_sequence: {process_sequence}, process_id: {process_id}".format(operation=operation, name=__name__, handle=self.db_handle, system_name=system_name, wabco_number=wabco_number, process_sequence=process_sequence, process_id=process_id))
        
        identification_buf = Identification()
        result = self.library.IdentifyMe(self.db_handle, system_name, wabco_number, process_sequence, process_id, byref(identification_buf))
        identification = {
                'processId': identification_buf.processId, 
                'systemId': identification_buf.systemId,
                'processStepId': identification_buf.processStepId,
                'wabcoPartId': identification_buf.wabcoPartId,
        }
            
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, system_name: {system_name}, wabco_number: {wabco_number}, process_sequence: {process_sequence}, process_id: {process_id}, identification: {identification}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, system_name=system_name, wabco_number=wabco_number, process_sequence=process_sequence, process_id=process_id, identification=identification)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))
            
        return [result, identification]    


    @error_wrap
    def get_production_lines(self):
        """
        RetVal GetProductionLines ( dbHandle handle, ProductionLinePtr **productionlines, int *countPtr )
        This function returns all available production lines.
        Parameter:
            handle is an Integer, that is returned by the function Login() when a new connection is created.
            productionlines is a pointer in which the production lines are returned as an array of pointers on ProductionLine structures, if the returncode is 0.
            typedef struct ProductionLine {
                idbID    id;                // Id of Record    
                char    description[514];        // Translated description
            } *ProductionLinePtr;
            countPtr is a pointer on an Integer, which returns the number of records in *productionlines, if the Returncode is 0.
        Returncodes:
            0    No Error
            < 0    ORACLE Error code
            6 (ERROR_INVALID_HANDLE) in case of an invalid handle
        
        @return systems - hash of systems   
        """
        operation = "Getting All Production Lines"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        productionLinePtr = pointer(ProductionLinePtr())
        result = self.library.GetProductionLines(self.db_handle, byref(productionLinePtr), byref(countPtr))
        count = countPtr.value
        production_lines = {}
        for item in productionLinePtr[:count]:
            if item.contents is None:
                break
            entry = {
                    'id': item.contents.id, 
                    'description': item.contents.description,
            }
            production_lines[item.contents.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, production_lines: {production_lines}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, production_lines=production_lines)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return systems
        return [result, production_lines]


    @error_wrap
    def get_production_line(self, production_line_id):
        """
        RetVal GetProductionLine ( dbHandle handle, idbID productionlineId, ProductionLinePtr productionline )
        This function returns a productionline structure for a defined id.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            productionlineId is the id of the record that should be read.
            productionline is a pointer on a productionline structure, which is filled when the Returncode is 0. The structure must be defined in the calling program.
        Returncodes:
            0    No error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
            1403    Record not found
        
        @return production_line - hash
        """
        operation = "Getting production_line"
        logger.debug("{operation} {name}. Handle: {handle}, production_line_id: {production_line_id}".format(operation=operation, name=__name__, handle=self.db_handle, production_line_id=production_line_id))
        
        buf = ProductionLine()
        result = self.library.GetProductionLine(self.db_handle, production_line_id, byref(buf))
        ret = {
                'id': buf.id, 
                'description': buf.description,
        }
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, production_line_id: {production_line_id}, production_line: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, production_line_id=production_line_id, ret=ret)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, ret]

    @error_wrap
    def get_wabco_parts(self):
        """
        RetVal GetWabcoParts ( dbHandle handle, WabcoPartPtr **wabcoParts, int *countPtr )
        This function returns all available parts, sorted alphabetically by the Wabco Number. 
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            wabcoParts is a pointer in which the Parts are being returned in an array of pointers on WabcoPart structures, if the returncode is 0.
            typedef struct WabcoPart {
                idbID    id;            // Id of record
                idbID    workCenterId;    // Id of work center
                cdbID    contentId;        // Id of binary data
                cdbID    previewId;        // Id of preview for above binary
                char    mdReason[514];    // Reason of last change
                char    mdUser[22];        // Last changed by user
                char    mdTime[24];        // Date of last change
                char    productName[52];    // Name of the product
                char    wabcoNumber[12];    // The Wabco Number
            } *WabcoPartPtr;
            countPtr is a pointer on an Integer in which the number of records in *wabcoParts is being returned, if the returncode is 0.
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        
        @return parts - hash   
        """
        operation = "Reading all Parts"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        wabcoPartPtr = pointer(WabcoPartPtr())
        result = self.library.GetWabcoParts(self.db_handle, byref(wabcoPartPtr), byref(countPtr))
        count = countPtr.value
        parts = {}
        for item in wabcoPartPtr[:count]:
            if item.contents is None:
                break
            entry = {
                'id': item.contents.id, 
                'workCenterId': item.contents.workCenterId,
                'contentId': item.contents.contentId,
                'previewId': item.contents.previewId,
                'mdReason': item.contents.mdReason,
                'mdUser': item.contents.mdUser,
                'mdTime': item.contents.mdTime,
                'productName': item.contents.productName,
                'wabcoNumber': item.contents.wabcoNumber,
            }
            parts[item.contents.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, parts: {parts}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, parts=parts)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return systems
        return [result, parts]


    @error_wrap
    def get_wabco_part(self, wabco_part_id):
        """
        RetVal GetWabcoPart ( dbHandle handle, idbID wabcoPartId, WabcoPartPtr wabcoPart )
        This function returns a WabcoPart structure for a defined Id.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            wabcoPartId != -1 then it is the ID of the part to be read.
            wabcoPartId == -1 then return wabcoPart for defined wabcoPart.wabco_number  by calling program.
            wabcoPart is a pointer on a WabcoPart structure, if the returncode is 0. The structure must be defined in the calling program.
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
            1403    Record not found
        
        @return wabco_part - hash
        """
        operation = "Reading a Part"
        logger.debug("{operation} {name}. Handle: {handle}, wabco_part_id: {wabco_part_id}".format(operation=operation, name=__name__, handle=self.db_handle, wabco_part_id=wabco_part_id))
        
        buf = WabcoPart()
        result = self.library.GetWabcoPart(self.db_handle, wabco_part_id, byref(buf))
        ret = {
                'id': buf.id, 
                'workCenterId': buf.workCenterId,
                'contentId': buf.contentId,
                'previewId': buf.previewId,
                'mdReason': buf.mdReason,
                'mdUser': buf.mdUser,
                'mdTime': buf.mdTime,
                'productName': buf.productName,
                'wabcoNumber': buf.wabcoNumber,
        }
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, wabco_part_id: {wabco_part_id}, wabco_part: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, wabco_part_id=wabco_part_id, ret=ret)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, ret]

    
    def new_wabco_part(self, wabco_part):
        #TODO: implement
        pass

        
    def new_wabco_part_process(self, wabco_part_id, process_id):
        #TODO: implement
        pass
    
    @error_wrap
    def get_processes(self):
        """
        RetVal GetProcesses ( dbHandle handle, ProcessPtr **processes, int *countPtr )
        This function returns all released processes, sorted by their Id. 
        Attention: This function takes the IGNORERELEASEID preference into account.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            processes is a pointer in which the processes are returned as an array of pointers on process structures, if the returncode is 0.
            typedef struct Process {
                idbID    id;            // Id of record
                idbID    productionLineId;    // Id of production line
                idbID    releaseId;        // Id of release status
                cdbID    contentId;        // Id of binary data
                cdbID    previewId;        // Id of preview for binary
                char    mdReason[514];    // Reason for last change
                char    mdUser[22];        // Last change by user
                char    mdTime[24];        // Date of last change
                char    description[514];    // Translated description
            } *ProcessPtr;
            countPtr is a pointer on an Integer in which the number of records in *processes is being returned, if the returncode is 0.
        
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
                
        @return processes - data hash   
        """
        operation = "Reading all Processes"
        logger.debug("{operation} {name}. Handle: {handle}".format(operation=operation, name=__name__, handle=self.db_handle))
        
        countPtr = c_int()
        bufPtr = pointer(ProcessPtr())
        result = self.library.GetProcesses(self.db_handle, byref(bufPtr), byref(countPtr))
        count = countPtr.value
        ret = {}
        for item in bufPtr[:count]:
            if item.contents is None:
                break
            entry = {
                'id': item.contents.id, 
                'productionLineId': item.contents.productionLineId,
                'releaseId': item.contents.releaseId,
                'contentId': item.contents.contentId,
                'previewId': item.contents.previewId,
                'mdReason': item.contents.mdReason,
                'mdUser': item.contents.mdUser,
                'mdTime': item.contents.mdTime,
                'description': item.contents.description,
            }
            ret[item.contents.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, ret=ret)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return data
        return [result, ret]


    @error_wrap
    def get_process(self, ident):
        """
        RetVal GetProcess ( dbHandle handle, idbID processId, ProcessPtr process )
        This function returns a process structure for a defined Id, if this process is released.
        Attention: This function takes the IGNORERELEASEID preference into account.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            processId is the Id of the process to be read.
            process is a pointer on a process structure, which is filled when the Returncode is 0. The structure must be defined in the calling program.
            
        Returncodes:
            0    No Error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
            1403    Record not found
        
        @return process - data hash
        """
        operation = "Reading a Process"
        logger.debug("{operation} {name}. Handle: {handle}, ident: {ident}".format(operation=operation, name=__name__, handle=self.db_handle, ident=ident))
        
        buf = Process()
        result = self.library.GetProcess(self.db_handle, ident, byref(buf))
        ret = {
                'id': buf.id, 
                'productionLineId': buf.productionLineId,
                'releaseId': buf.releaseId,
                'contentId': buf.contentId,
                'previewId': buf.previewId,
                'mdReason': buf.mdReason,
                'mdUser': buf.mdUser,
                'mdTime': buf.mdTime,
                'description': buf.description,
        }
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, ident: {ident}, ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, ident=ident, ret=ret)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, ret]


    @error_wrap
    def get_wabco_part_processes(self, wabco_part_id):
        """
        RetVal GetWabcoPartProcesses ( dbHandle handle, idbID wabcoPartId, ProcessPtr **processes, int *countPtr )
        
        This function returns all released processes for a Wabco Number, sorted by their Id. 
        Attention: This function takes the IGNORERELEASEID preference into account.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            wabcoPartId is the Id of the part record. It can be found for a Wabco number with the aid of the function GetWabcoParts().
            processes is a pointer in which the processes are returned as an array of pointers on process structures, if the Returncode is 0.
            countPtr is a pointer on an Integer in which the number of records in *processes is being returned, if the Returncode is 0.
        Returncodes:
            0    No error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
                
        @return processes - data hash   
        """
        operation = "Reading all processes for a Wabco Number"
        ident = wabco_part_id
        logger.debug("{operation} {name}. Handle: {handle} Ident: {ident}".format(operation=operation, name=__name__, handle=self.db_handle, ident=ident))
        
        countPtr = c_int()
        bufPtr = pointer(ProcessPtr())
        result = self.library.GetWabcoPartProcesses(self.db_handle, ident, byref(bufPtr), byref(countPtr))
        count = countPtr.value
        ret = {}
        for item in bufPtr[:count]:
            if item.contents is None:
                break
            entry = {
                'id': item.contents.id, 
                'productionLineId': item.contents.productionLineId,
                'releaseId': item.contents.releaseId,
                'contentId': item.contents.contentId,
                'previewId': item.contents.previewId,
                'mdReason': item.contents.mdReason,
                'mdUser': item.contents.mdUser,
                'mdTime': item.contents.mdTime,
                'description': item.contents.description,
            }
            ret[item.contents.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, ident: {ident} ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, ret=ret, ident=ident)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return data
        return [result, ret]

    @error_wrap
    def get_process_steps(self, process_id):
        """
        RetVal GetProcessSteps    ( dbHandle handle, idbID processId, ProcessStepPtr **processSteps, int *countPtr )
        
        This function returns all released process steps for a defined process, sorted by their sequence. 
        Attention: This function takes the IGNORERELEASEID preference into account.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            processId is the Id of the released process, for which the Process Steps should be found.
            processSteps is a pointer in which the process steps are returned as an array of pointers on ProcessStep structures, if the returncode is 0.
            typedef struct ProcessStep {
                idbID    id;            // Id of record
                idbID    processId;        // Id of the process
                idbID    systemId;        // Id of the system record
                idbID    releaseId;         // Id of release status
                int    processSequence;    // Process sequence number
                double limitYellow;    // Yellow warning level
                double limitRed;        // red warning level
                char    mdReason[514];    // Reason of last change
                char    mdUser[22];        // Last change user
                char    mdTime[24];        // Date of last change
                char    filename[258];    // A Filenams
                char    transfer[2];    // Transfer
                char    description[514];    // Translated description
            } *ProcessStepPtr;
            countPtr is a pointer on an Integer in which the number of records in *processSteps is being returned, if the Returncode is 0.
        
        Returncodes:
            0    No error
            < 0    ORACLE error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
                
        @return process_steps - data hash   
        """
        operation = "Read All Process Steps for a given process"
        ident = process_id
        logger.debug("{operation} {name}. Handle: {handle} Ident: {ident}".format(operation=operation, name=__name__, handle=self.db_handle, ident=ident))
        
        countPtr = c_int()
        bufPtr = pointer(ProcessStepPtr())
        result = self.library.GetProcessSteps(self.db_handle, ident, byref(bufPtr), byref(countPtr))
        count = countPtr.value
        ret = {}
        for item in bufPtr[:count]:
            if item.contents is None:
                break
            buf = item.contents
            entry = {
                'id': buf.id, 
                'processId': buf.processId,
                'systemId': buf.systemId,
                'releaseId': buf.releaseId,
                'processSequence': buf.processSequence,
                'limitYellow': buf.limitYellow,
                'limitRed': buf.limitRed,
                'mdReason': buf.mdReason,
                'mdUser': buf.mdUser,
                'mdTime': buf.mdTime,
                'filename': buf.filename,
                'transfer': buf.transfer,
                'description': buf.description,
            }
            ret[buf.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, ident: {ident} ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, ret=ret, ident=ident)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return data
        return [result, ret]

    @error_wrap
    def get_process_step(self, ident):
        """
        RetVal GetProcessStep    ( dbHandle handle, idbID processStepId, ProcessStepPtr processStep )
        This function returns a ProcessStep structure for a defined Id, if the Process Step is released.
        Attention: This function takes the IGNORERELEASEID preference into account.
        Parameter:
        handle is an Integer, which is returned by the function Login() at the creation of a new connection.
        processStepId is the Id of the process Step to be read.
        processStep is a pointer on a ProcessStep structure that is filled if the returncode is 0. the structure must be defined in the calling program.
        
        Returncodes:
        0    No error
        < 0    ORACLE Error code
        6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        1403    Record not found
        
        @return process_step - data hash
        """
        operation = "Reading a Process Step"
        logger.debug("{operation} {name}. Handle: {handle}, ident: {ident}".format(operation=operation, name=__name__, handle=self.db_handle, ident=ident))
        
        buf = ProcessStep()
        result = self.library.GetProcessStep(self.db_handle, ident, byref(buf))
        ret = {
                'id': buf.id, 
                'processId': buf.processId,
                'systemId': buf.systemId,
                'releaseId': buf.releaseId,
                'processSequence': buf.processSequence,
                'limitYellow': buf.limitYellow,
                'limitRed': buf.limitRed,
                'mdReason': buf.mdReason,
                'mdUser': buf.mdUser,
                'mdTime': buf.mdTime,
                'filename': buf.filename,
                'transfer': buf.transfer,
                'description': buf.description,
        }
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, ident: {ident}, ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, ident=ident, ret=ret)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, ret]


    @error_wrap
    def get_process_step_params(self, process_step_id):
        #TODO: check why does not work!!! does it?
        """
        RetVal GetProcessStepParams    ( dbHandle handle, idbID processStepId, ProcessStepParamPtr **processStepParams, int *countPtr )
        
        This function returns all process step parameter for a defined Process Step, sorted by their sequence. Please note: For a correct behaviour concerning the legacy data, the field HISTORY is analysed within the selection (HISTORY = 1).
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            processStepId is the Id of the released process step, whose process step parameter shall be found.
            processStepParam is a pointer, in which the process step parameters are being returned in an array of pointers on ProcessStepParam structures, if the returncode is 0.
            typedef struct ProcessStepParam {
                idbID    id;            // Id of record
                idbID    processStepId;    // Id of process step record
                idbID    unitId;        // Id of unit record
                cdbID    contentId;        // Id of binary data
                cdbID    previewId;        // Id of preview for above binary
                double value;        // The Value
                char    valueText[258];    // Additional value as text
                int    paramSequence;    // The parameter sequence number
                int    history;        // History flag
                char    mdReason[514];    // Reason of last change
                char    mdUser[22];        // Last change user
                char    mdTime[24];        // Date of last change
                char    description[514];    // Translated description
            } *ProcessStepParamPtr;
            countPtr is a pointer on an Integer which returns the number of records in *processStepParams, if the returncode is 0.
        
        Returncodes:
            0    No error
            < 0    ORACLE Error code
            6    (ERROR_INVALID_HANDLE) in case of an invalid handle
                
        @return process_step_params - data hash   
        """
        operation = "Reading all Process Step Parameters"
        ident = process_step_id
        logger.debug("{operation} {name}. Handle: {handle} Ident: {ident}".format(operation=operation, name=__name__, handle=self.db_handle, ident=ident))
        
        countPtr = c_int()
        bufPtr = pointer(ProcessStepParamPtr())
        result = self.library.GetProcessStepParams(self.db_handle, ident, byref(bufPtr), byref(countPtr))
        count = countPtr.value
        ret = {}
        for item in bufPtr[:count]:
            if item.contents is None:
                break
            buf = item.contents
            entry = {
                'id': buf.id,
                'processStepId': buf.processStepId,
                'unitId': buf.unitId,
                'contentId': buf.contentId,
                'previewId': buf.previewId,
                'value': buf.value,
                'valueText': buf.valueText,
                'paramSequence': buf.paramSequence,
                'history': buf.history,
                'mdReason': buf.mdReason,
                'mdUser': buf.mdUser,
                'mdTime': buf.mdTime,
                'description': buf.description,
            }
            ret[buf.id] = entry

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, count: {count}, ident: {ident} ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, count=count, ret=ret, ident=ident)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return data
        return [result, ret]


    @error_wrap
    def new_process_step_param(self, process_step_param):
        # TODO: FIXME.
        """
        RetVal NewProcessStepParam ( dbHandle handle, ProcessStepParamPtr processStepParam)
        This function creates process step parameter. Fields in ProcessStepParam structure:
            id - only returned value, nextval from PRODANG.PROCESS_STEP_PARAM_SEQ sequence
            processStepId - ProcessStep.id
            unitId - possible values can be read by GetUnits function, 0 = no UNIT
            contentId - opaque_data.id; = no contentId
            previewId - opaque_data.id; = no data previewId
            value - value
            valueText - text as value, no valueText
            paramSequence - test step parameter sequence, -1 = automatic
            history - only returned value, 0-active test value, 1-historical (not active) test value
            mdReason -  reason of modification, mdReason=created by <actual Oracle user>
            mdUser - only returned value, actual Oracle user
            mdTime - only returned value, actual Oracle sysdate
            description - description for test value, mdReason=no description
        
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            processStepParam is a pointer on a ProcessStepParam structure, which contains the data. The structure must be defined in the calling program. It is being returned with the new record.
        
        Returncodes:
            0    No error
            < 0    ORACLE Error code
            6 (ERROR_INVALID_HANDLE) in case of an invalid handle
            234    (ERROR_MORE_DATA) when process step parameter with the same paramSequence exist
                
        @return Null   
        """
        operation = "Adding Process Step Parameter"
        data = process_step_param
        logger.debug("{operation} {name}. Handle: {handle} data: {data}".format(operation=operation, name=__name__, handle=self.db_handle, data=data))
        
        dataObj = ProcessStepParam(
            id=data['id'],
            processStepId=data['processStepId'],
            unitId=data['unitId'],
            contentId=data['contentId'],
            previewId=data['previewId'],
            value=data['value'],
            valueText=data['valueText'],
            paramSequence=data['paramSequence'],
            history=data['history'],
            mdReason=data['mdReason'],
            mdUser=data['mdUser'],
            mdTime=data['mdTime'],
            description=data['description'],
        )
                                            
        result = self.library.NewProcessStepParam(self.db_handle, dataObj)  

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, data: {data}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, data=data)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return data
        return [result, None]
    
    
    @error_wrap
    def new_product(self, wabco_part_id, serial_number, individual=1, comment="empty comment"):
        """
        RetVal NewProduct ( dbHandle handle, ProductPtr product )
        RetVal NewProduct_lsn ( dbHandle handle, Product_lsnPtr product )

        This function creates a new Product out of a prefilled product structure.
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            product is a pointer on a product structure, which elements must be prefilled. The structure must be defined, filled in the calling program. Before set value for struct members clean the structure ex. memset(&product, 0, sizeof(product)) , cleaning structure will set default values for optional struct members. The function checks if a product with the passed WabcoPartId and serial number already exists and returns this. In this case no new product record is created.
            If returncode=ERROR_MORE_DATA, the existing record (for defined wabcoPartId and serialNumber) is returned unchanged.
            If returncode=0, the new record is returned.

        Required: wabcoPartId, serialNumber, individual
        Optional: comment (default=null), crProcessStepId (default=null), crTime (default=sysdate), mdTime (default=crTime)
        Returncodes:
            0        No error
            234      (ERROR_MORE_DATA) in case that the product already exists. This is no error and the product structure is returned with the existing product. 
            < 0      ORACLE Error code
            6        (ERROR_INVALID_HANDLE) in case of an invalid handle                
        @return Null   
        """
        operation = "Adding Product"
        data = str(wabco_part_id) + str(serial_number)
        logger.debug("{operation} {name}. Handle: {handle} data: {data}".format(operation=operation, name=__name__, handle=self.db_handle, data=data))

        """
            /*
            Product generating
                Required: wabcoPartId, serialNumber, individual
                Optional: comment (default=null), crProcessStepId (default=null), crTime (default=sysdate), mdTime (default=crTime)
            */
            memset(&product, 0, sizeof(product)); // clear product structure
            product.wabcoPartId=ident.wabcoPartId; // set wabco part id
            strcpy(product.serialNumber,serial_number); // serial number for product
            product.individual=1; // set whether product is with SN (individual=1) or without SN (individual=0)
            product.crProcessStepId=ident.processStepId; // set creating process step
            strcpy(product.comment,"added from test program, v. 1.234"); // comment for product, ex. version of test program
        
            r = NewProduct_lsn(h1,&product); // create product        
        """
        
        dataObj = Product( 
                    wabcoPartId = wabco_part_id,
                    serialNumber = serial_number,
                    individual = individual, 
                    comment = comment,
        )
        
        print dataObj
        result = self.library.NewProduct_lsn(self.db_handle, dataObj)  

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, data: {data}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, data=data)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        #return data
        return [result, None]

    
    @error_wrap
    def get_product(self, wabco_part_id, serial_number):
        """
        RetVal GetProduct    ( dbHandle handle, idbID wabcoPartId, 
        char* serialNumber, ProductPtr product )
        RetVal GetProduct_lsn    ( dbHandle handle, idbID wabcoPartId, 
        char* serialNumber, Product_lsnPtr product )

        This function returns a product structure for a product, which can be defined in three ways:
        1. wabcoPartId != -1 then search using wabcoPartId and serialNumber
        2. wabcoPartId == -1and product->id !='' then search using product->id
        3. wabcoPartId == -1and product->id =='' then search using serialNumber
        Important information: The field 'individual' was taken over from the field 'allgemein' of the legacy data directly. Because of this most products have the value 0 further on and only a few the value 1. 
        
        Parameter:
            handle is an Integer, which is returned by the function Login() at the creation of a new connection.
            wabcoPartId is the Id of the part.
            serialNumber is the serial number of the product for the part above.
            product is a pointer on a product structure, which is filled if the returncode is 0. The structure must be defined in the calling program.
            typedef struct Product {
                cdbID    id;            // Id of record
                idbID    wabcoPartId;    // Id of Wabco Part record
                char    serialNumber[32];    // Serial number
                char    comment[258];    // A comment
                int    individual;        // Individual flag
                idbID    crProcessStepId;    // Id of creating process step
                idbID    mdProcessStepId;    // Id of modifying process step
                char    crTime[24];        // Date of creation
                char    mdTime[24];        // Date of last change
            } *ProductPtr;
            typedef struct Product_lsn {
                cdbID    id;            // Id of record
                idbID    wabcoPartId;    // Id of Wabco Part record
                char    serialNumber[1002];    // Long Serial number
                char    comment[258];    // A comment
                int    individual;        // Individual flag
                idbID    crProcessStepId;    // Id of creating process step
                idbID    mdProcessStepId;    // Id of modifying process step
                char    crTime[24];        // Date of creation
                char    mdTime[24];        // Date of last change
            } *Product_lsnPtr;

        Returncodes:
        0    No error
        < 0    ORACLE Error code
        6    (ERROR_INVALID_HANDLE) in case of an invalid handle
        1403    Record does not exist
        
        @return process - data hash
        """
        operation = "Reading a Product"
        ident = str(wabco_part_id) + str(serial_number)
        logger.debug("{operation} {name}. Handle: {handle}, ident: {ident}".format(operation=operation, name=__name__, handle=self.db_handle, ident=ident))
        
        buf = Product()
        result = self.library.GetProduct(self.db_handle, wabco_part_id, serial_number, byref(buf))
        ret = {
                'id': buf.id, 
                'wabcoPartId': buf.wabcoPartId,
                'serialNumber': buf.serialNumber,
                'comment': buf.comment,
                'individual': buf.individual,
                'crProcessStepId': buf.crProcessStepId,
                'mdProcessStepId': buf.mdProcessStepId,
                'crTime': buf.crTime,
                'mdTime': buf.mdTime,
        }
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, ident: {ident}, ret: {ret}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, ident=ident, ret=ret)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return [result, ret]
    
    
