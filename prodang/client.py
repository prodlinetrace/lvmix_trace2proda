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
from prodang.types import dbHandle, ProdaNGObject, LanguageData, LanguageDataPtr

logger = logging.getLogger(__name__)


def error_wrap(func):
    """Parses a prodang error code returned the decorated function."""
    def f(*args, **kw):
        returned_items = func(*args, **kw)
        code = returned_items[0]
        #print "items", returned_items, "code", code
        check_error(code, context=func.__name__)
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
        
        return (result, self.db_handle)

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
                    
        return (result, None)

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
                    
        return (result, None)
        

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
                    
        return (result, None)


    @error_wrap
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
        result = self.library.GetLastErrorMsg(self.db_handle)
        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}".format(operation=operation, result=result, name=__name__, handle=self.db_handle)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                
        return (result, None)


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

        return (result, struct_datetime)


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
                    'name': item.contents.name
                    }
            languages[item.contents.id] = lang

        log_msg = "Result: {result}, Operation:{operation}, Func_name: {name}. Handle: {handle}, lang_count: {lang_count}, languages: {languages}".format(operation=operation, result=result, name=__name__, handle=self.db_handle, lang_count=lang_count, languages=languages)
        if result == 0:
            logger.info("Successful. {msg}".format(msg=log_msg))
        else: 
            logger.error("Failed. {msg}".format(msg=log_msg))                

        return (result, languages)

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
                    
        return (result, None)
        

    







'''

    def plc_stop(self):
        """
        stops a client
        """
        logger.info("stopping plc")
        return self.library.Cli_PlcStop(self.pointer)

    def plc_cold_start(self):
        """
        cold starts a client
        """
        logger.info("cold starting plc")
        return self.library.Cli_PlcColdStart(self.pointer)

    def plc_hot_start(self):
        """
        hot starts a client
        """
        logger.info("hot starting plc")
        return self.library.Cli_PlcColdStart(self.pointer)

    @error_wrap
    def disconnect(self):
        """
        disconnect a client.
        """
        logger.info("disconnecting snap7 client")
        return self.library.Cli_Disconnect(self.pointer)

    @error_wrap
    def connect(self, address, rack, slot, tcpport=102):
        """
        Connect to a S7 server.

        :param address: IP address of server
        :param rack: rack on server
        :param slot: slot on server.
        """
        logger.debug("connecting to %s:%s rack %s slot %s" % (address, tcpport,
                                                             rack, slot))

        self.set_param(snap7.snap7types.RemotePort, tcpport)
        return self.library.Cli_ConnectTo(
            self.pointer, c_char_p(six.b(address)),
            c_int(rack), c_int(slot))

    def db_read(self, db_number, start, size):
        """This is a lean function of Cli_ReadArea() to read PLC DB.

        :returns: user buffer.
        """
        logger.debug("db_read, db_number:%s, start:%s, size:%s" %
                     (db_number, start, size))

        type_ = snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]
        data = (type_ * size)()
        result = (self.library.Cli_DBRead(
            self.pointer, db_number, start, size,
            byref(data)))
        check_error(result, context="client")
        return bytearray(data)

    @error_wrap
    def db_write(self, db_number, start, data):
        """
        Writes to a DB object.

        :param start: write offset
        :param data: bytearray
        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        size = len(data)
        cdata = (type_ * size).from_buffer(data)
        logger.debug("db_write db_number:%s start:%s size:%s data:%s" %
                     (db_number, start, size, data))
        return self.library.Cli_DBWrite(self.pointer, db_number, start, size,
                                        byref(cdata))

    def full_upload(self, _type, block_num):
        """
        Uploads a full block body from AG.
        The whole block (including header and footer) is copied into the user
        buffer.

        :param block_num: Number of Block
        """
        _buffer = buffer_type()
        size = c_int(sizeof(_buffer))
        block_type = snap7.snap7types.block_types[_type]
        result = self.library.Cli_FullUpload(self.pointer, block_type,
                                             block_num, byref(_buffer),
                                             byref(size))
        check_error(result, context="client")
        return bytearray(_buffer), size.value

    def upload(self, block_num):
        """
        Uploads a block body from AG

        :param data: bytearray
        """
        logger.debug("db_upload block_num: %s" % (block_num))

        block_type = snap7.snap7types.block_types['DB']
        _buffer = buffer_type()
        size = c_int(sizeof(_buffer))

        result = self.library.Cli_Upload(self.pointer, block_type, block_num,
                                         byref(_buffer), byref(size))

        check_error(result, context="client")
        logger.info('received %s bytes' % size)
        return bytearray(_buffer)

    @error_wrap
    def download(self, data, block_num=-1):
        """
        Downloads a DB data into the AG.
        A whole block (including header and footer) must be available into the
        user buffer.

        :param block_num: New Block number (or -1)
        :param data: the user buffer
        """
        type_ = c_byte
        size = len(data)
        cdata = (type_ * len(data)).from_buffer(data)
        result = self.library.Cli_Download(self.pointer, block_num,
                                           byref(cdata), size)
        return result

    def db_get(self, db_number):
        """Uploads a DB from AG.
        """
        # logger.debug("db_get db_number: %s" % db_number)
        _buffer = buffer_type()
        bufferSize = c_int(snap7.snap7types.buffer_size)
        result = self.library.Cli_DBGet(
            self.pointer, db_number, byref(_buffer),
            byref(bufferSize))
        check_error(result, context="client")
        msg = bytearray(_buffer[:bufferSize.value])
        return msg

    def read_area(self, area, dbnumber, start, size):
        """This is the main function to read data from a PLC.
        With it you can read DB, Inputs, Outputs, Merkers, Timers and Counters.

        :param dbnumber: The DB number, only used when area= S7AreaDB
        :param start: offset to start writing
        :param size: number of units to read
        """
        assert area in snap7.snap7types.areas.values()
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        logger.debug("reading area: %s dbnumber: %s start: %s: amount %s: wordlen: %s" % (area, dbnumber, start, size, wordlen))
        data = (type_ * size)()
        result = self.library.Cli_ReadArea(self.pointer, area, dbnumber, start,
                                           size, wordlen, byref(data))
        check_error(result, context="client")
        return bytearray(data)

    @error_wrap
    def write_area(self, area, dbnumber, start, data):
        """This is the main function to write data into a PLC. It's the
        complementary function of Cli_ReadArea(), the parameters and their
        meanings are the same. The only difference is that the data is
        transferred from the buffer pointed by pUsrData into PLC.

        :param dbnumber: The DB number, only used when area= S7AreaDB
        :param start: offset to start writing
        :param data: a bytearray containing the payload
        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        size = len(data)
        logger.debug("writing area: %s dbnumber: %s start: %s: size %s: type: %s" % (area, dbnumber, start, size, type_))
        cdata = (type_ * len(data)).from_buffer(data)
        return self.library.Cli_WriteArea(self.pointer, area, dbnumber, start,
                                          size, wordlen, byref(cdata))

    def read_multi_vars(self, items):
        """This function read multiple variables from the PLC.

        :param items: list of S7DataItem objects
        :returns: a tuple with the return code and a list of data items
        """
        result = self.library.Cli_ReadMultiVars(self.pointer, byref(items),
                                                c_int32(len(items)))
        check_error(result, context="client")
        return result, items

    def list_blocks(self):
        """Returns the AG blocks amount divided by type.

        :returns: a snap7.types.BlocksList object.
        """
        # logger.debug("listing blocks")
        blocksList = BlocksList()
        result = self.library.Cli_ListBlocks(self.pointer, byref(blocksList))
        check_error(result, context="client")
        logger.debug("blocks: %s" % blocksList)
        return blocksList

    def list_blocks_of_type(self, blocktype, size=1024):
        """This function returns the AG list of a specified block type."""
        # logger.debug("listing blocks of type: %s size: %s" % (blocktype, size))
        _buffer = (snap7.types.word * size)()
        count = c_int(size)
        result = self.library.Cli_ListBlocksOfType(
            self.pointer, blocktype,
            byref(_buffer),
            byref(count))

        # logger.debug("number of items found: %s" % count.value)
        check_error(result, context="client")
        return _buffer[:count.value]

    @error_wrap
    def set_session_password(self, password):
        """Send the password to the PLC to meet its security level."""
        assert len(password) <= 8, 'maximum password length is 8'
        return self.library.Cli_SetSessionPassword(self.pointer,
                                                   c_char_p(six.b(password)))

    @error_wrap
    def clear_session_password(self):
        """Clears the password set for the current session (logout)."""
        return self.library.Cli_ClearSessionPassword(self.pointer)

    def set_connection_params(self, address, local_tsap, remote_tsap):
        """
        Sets internally (IP, LocalTSAP, RemoteTSAP) Coordinates.
        This function must be called just before Cli_Connect().

        :param address: PLC/Equipment IPV4 Address, for example "192.168.1.12"
        :param local_tsap: Local TSAP (PC TSAP)
        :param remote_tsap: Remote TSAP (PLC TSAP)
        """
        assert re.match(ipv4, address), '%s is invalid ipv4' % address
        result = self.library.Cli_SetConnectionParams(self.pointer, address,
                                                      c_uint16(local_tsap),
                                                      c_uint16(remote_tsap))
        if result != 0:
            raise Snap7Exception("The parameter was invalid")

    def set_connection_type(self, connection_type):
        """
        Sets the connection resource type, i.e the way in which the Clients
        connects to a PLC.

        :param connection_type: 1 for PG, 2 for OP, 3 to 10 for S7 Basic
        """
        result = self.library.Cli_SetConnectionType(self.pointer,
                                                    c_uint16(connection_type))
        if result != 0:
            raise Snap7Exception("The parameter was invalid")

    def get_connected(self):
        """
        Returns the connection status

        :returns: a boolean that indicates if connected.
        """
        connected = c_int32()
        result = self.library.Cli_GetConnected(self.pointer, byref(connected))
        check_error(result, context="client")
        return bool(connected)

    def ab_read(self, start, size):
        """
        This is a lean function of Cli_ReadArea() to read PLC process outputs.
        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        data = (type_ * size)()
        logger.debug("ab_read: start: %s: size %s: " % (start, size))
        result = self.library.Cli_ABRead(self.pointer, start, size,
                                         byref(data))
        check_error(result, context="client")
        return bytearray(data)

    def ab_write(self, start, data):
        """
        This is a lean function of Cli_WriteArea() to write PLC process
        outputs
        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        size = len(data)
        cdata = (type_ * size).from_buffer(data)
        logger.debug("ab write: start: %s: size: %s: " % (start, size))
        return self.library.Cli_ABWrite(
            self.pointer, start, size, byref(cdata))

    def as_ab_read(self, start, size):
        """
        This is the asynchronous counterpart of client.ab_read().
        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        data = (type_ * size)()
        logger.debug("ab_read: start: %s: size %s: " % (start, size))
        result = self.library.Cli_AsABRead(self.pointer, start, size,
                                           byref(data))
        check_error(result, context="client")
        return bytearray(data)

    def as_ab_write(self, start, data):
        """
        This is the asynchronous counterpart of Cli_ABWrite.
        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        size = len(data)
        cdata = (type_ * size).from_buffer(data)
        logger.debug("ab write: start: %s: size: %s: " % (start, size))
        return self.library.Cli_AsABWrite(
            self.pointer, start, size, byref(cdata))

    @error_wrap
    def as_compress(self, time):
        """
        This is the asynchronous counterpart of client.compress().
        """
        return self.library.Cli_AsCompress(self.pointer, time)

    def copy_ram_to_rom(self):
        """

        """
        return self.library.Cli_AsCopyRamToRom(self.pointer)

    def as_ct_read(self):
        """

        """
        return self.library.Cli_AsCTRead(self.pointer)

    def as_ct_write(self):
        """

        """
        return self.library.Cli_AsCTWrite(self.pointer)

    def as_db_fill(self):
        """

        """
        return self.library.Cli_AsDBFill(self.pointer)

    def as_db_get(self, db_number):
        """
        This is the asynchronous counterpart of Cli_DBGet.
        """
        # logger.debug("db_get db_number: %s" % db_number)
        _buffer = buffer_type()
        bufferSize = c_int(snap7.snap7types.buffer_size)
        result = self.library.Cli_AsDBGet(self.pointer, db_number, byref(_buffer), byref(bufferSize))
        check_error(result, context="client")
        msg = bytearray(_buffer[:bufferSize.value])
        return msg

    def as_db_read(self, db_number, start, size):
        """
        This is the asynchronous counterpart of Cli_DBRead.

        :returns: user buffer.
        """
        # logger.debug("db_read, db_number:%s, start:%s, size:%s" % (db_number, start, size))

        type_ = snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]
        data = (type_ * size)()
        result = (self.library.Cli_AsDBRead(self.pointer, db_number, start, size, byref(data)))
        check_error(result, context="client")
        return bytearray(data)

    def as_db_write(self, db_number, start, data):
        """

        """
        wordlen = snap7.snap7types.S7WLByte
        type_ = snap7.snap7types.wordlen_to_ctypes[wordlen]
        size = len(data)
        cdata = (type_ * size).from_buffer(data)
        logger.debug("db_write db_number:%s start:%s size:%s data:%s" %
                     (db_number, start, size, data))
        return self.library.Cli_AsDBWrite(self.pointer, db_number, start, size, byref(cdata))

    @error_wrap
    def as_download(self, data, block_num=-1):
        """
        Downloads a DB data into the AG asynchronously.
        A whole block (including header and footer) must be available into the
        user buffer.

        :param block_num: New Block number (or -1)
        :param data: the user buffer
        """
        size = len(data)
        type_ = c_byte * len(data)
        cdata = type_.from_buffer(data)
        return self.library.Cli_AsDownload(self.pointer, block_num,
                                           byref(cdata), size)

    @error_wrap
    def compress(self, time):
        """
        Performs the Memory compress action.

        :param time: Maximum time expected to complete the operation (ms).
        """
        return self.library.Cli_Compress(self.pointer, time)

    @error_wrap
    def set_param(self, number, value):
        """Sets an internal Server object parameter.
        """
        logger.debug("setting param number %s to %s" % (number, value))
        type_ = param_types[number]
        return self.library.Cli_SetParam(self.pointer, number,
                                         byref(type_(value)))

    def get_param(self, number):
        """Reads an internal Client object parameter.
        """
        logger.debug("retrieving param number %s" % number)
        type_ = param_types[number]
        value = type_()
        code = self.library.Cli_GetParam(self.pointer, c_int(number),
                                         byref(value))
        check_error(code)
        return value.value

    def get_plc_date_time(self):
        """
        Gets the time structure from PLC and transforms it to python's time.struct_time

        # internal PLC DateTime struct
        typedef struct
        {
          int   tm_sec;
          int   tm_min;
          int   tm_hour;
          int   tm_mday;
          int   tm_mon;
          int   tm_year;
          int   tm_wday;
          int   tm_yday;
          int   tm_isdst;
        }tm;
        """
        logger.debug("retrieving DateTime from PLC")
        result = self.library.Cli_GetPlcDateTime(self.pointer, byref(time_struct_buf))
        check_error(result, context="client")
        st = snap7.util.bytearray_2_time_struct(time_struct_buf)
        logger.debug("DateTime from PLC received %s", st)
        return st

    @error_wrap
    def set_plc_date_time(self, dtime):
        """
        Sets the time to given value.
        Use datetime.datetime as input format.
        """

        logger.debug("Setting system Date/Time on PLC to: %s" % (dtime))
        buf = snap7.util.time_struct_2_bytearray(dtime)
        return self.library.Cli_SetPlcDateTime(self.pointer, byref(buf))

    @error_wrap
    def set_plc_system_date_time(self):
        """
        Synchronizes OS time with PLC
        """
        import datetime
        logger.debug("Updating System DateTime to PLC: (PC->PLC) %s" % datetime.datetime.now())
        return self.library.Cli_SetPlcSystemDateTime(self.pointer)
'''