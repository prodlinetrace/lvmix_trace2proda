#ifndef ProdaNG_DLLH
#define ProdaNG_DLLH         // Borland C++Builder expects #ifndef ProdaNG_DLLH and
                             // #define ProdaNG_DLLH dereived form the filename
#undef ProdaNG_DLLH          // for multiple includes, but be carefull!!!
//
// Definition of ProdaNG DLL
//
// History:
//
// Version 1.1 07.07.2006       Markus Hess (A&L) Initial version
// Version 2.0 25.10.2006       Günter Morlang    Common use for DLL-generation and usage
// Version 2.1 07.09.2007       Günter Morlang    #define .._SIZE-constants added
// Version 2.2 26.10.2007       Markus Hess (A&L) New functions for opacque data result table
// Version 2.3 29.02.2008       Günter Morlang    New functions:
//                                                - FreeData( void **data ) in ProdaNG_DLL.pc
//                                                - GetProductionLine, GetProductionLines in masterdata.pc
//                                                New struct ProductionLine in ProdaNG_DLL.h
// Version 2.4 03.03.2008       Günter Morlang    Preference "IGNORERELEASEID" added 
// Versoim 2.5 13.03.2008		Markus Hess (A&L) Fixed comment typos and indenting for VS
// Versoim 2.6 06.05.2008		Markus Hess (A&L) New function GetPreviousProcessStepStatus
// Version 2.7 12.12.2008		Maciej Iwanczewski New function GetTestSteps_orderby
// Version 2.7.0.1 18.12.2008	Maciej Iwanczewski New status: -3 to automaticly set status 100+standard status=100,101,105... for devices which should not be used in statistical analysis (prototypes/testbench test)
// Version 3.0 29.04.2010		Maciej Iwanczewski New functions: New/Set/DeleteProcessStepParam, New/Set/DeleteTestStepParam, New/Set/DeleteTestStep, New/Set/DeleteTestValue, NewWabcoPart, NewWabcoPart_Process
// Version 3.1 20.03.2012		Maciej Iwanczewski New function UpdateWabcoNumber
// Version 3.2 10.07.2013		Maciej Iwanczewski Update SetTestStepResult and SetProcessStepResult
// Version 3.3 18.09.2013		Maciej Iwanczewski add dedicated functions for WPL EAPU line (eapu.pc file)
// Version 3.5 20.05.2014		Maciej Iwanczewski extend serial number field size, add functions to manage componets, add _lsn functions to manage products with loong serial numbers
// Standard Return Codes:
//
// 0				OK
// Oracle Errors	< 0 or 1403 (No record found)
// Windows error code ERROR_INVALID_HANDLE in case of an invalid handle
//
// Other error codes are documented in the function declaration and definition comments
//

#if !defined(__PRODADLL_EXPORT__) && !defined(__PRODADLL_IMPORT__) && \
    !defined(__PRODADLL_PASS_1__) && !defined(__PRODADLL_PASS_2__) && !defined( __PRODADLL_TYPEDEF__)
#define __PRODADLL_EXPORT__
#endif

//******************************************************************************
//******************************************************************************
// Typedef-section of header
#if defined(__PRODADLL_EXPORT__) || defined(__PRODADLL_IMPORT__) || \
    defined(__PRODADLL_PASS_1__) || defined(__PRODADLL_TYPEDEF__)

// char size definitions
#define PRODANGDLL_CDBID_SIZE               16
#define PRODANGDLL_ISOCODE_SIZE             34
#define PRODANGDLL_LANGUAGEDATA_NAME_SIZE   66
#define PRODANGDLL_DESCRIPTION_SIZE        514
#define PRODANGDLL_MIMETYPE_SIZE           130
#define PRODANGDLL_UNITNAME_SIZE            12
#define PRODANGDLL_MDREASON_SIZE           514
#define PRODANGDLL_MDUSER_SIZE              22
#define PRODANGDLL_SYSTEM_NAME_SIZE         52
#define PRODANGDLL_PRODUCTNAME_SIZE         52
#define PRODANGDLL_WABCONUMBER_SIZE         12
#define PRODANGDLL_FILENAME_SIZE           258
#define PRODANGDLL_TRANSFER_SIZE             2
#define PRODANGDLL_VALUETEXT_SIZE          258
#define PRODANGDLL_SERIALNUMBER_SIZE      32
#define PRODANGDLL_SERIALNUMBER_SIZE_LSN   1002
#define PRODANGDLL_COMMENT_SIZE            258
#define PRODANGDLL_MDTIME_SIZE              24
#define PRODANGDLL_CRTIME_SIZE              24
#define PRODANGDLL_STARTTIME_SIZE           24
#define PRODANGDLL_ENDTIME_SIZE             24
#define GETTESTSTEPS_ORDERBY_TEST_SEQUENCE  0 // used for function GetTestSteps_orderby
#define GETTESTSTEPS_ORDERBY_TEST_ORDER     1 // used for function GetTestSteps_orderby


typedef INT32 RetVal;	// Standard return value type

typedef INT32 dbHandle;	// Context Handle type

typedef char cdbID[ PRODANGDLL_CDBID_SIZE ];
            // Character-reprsentation for database ID's also usable in SPS software
						// This will cause a little bit overhead in the DLL but has the advantage to use high numbered IDs
						// To signal an unknown id, the string "-1" is used. This refers to the row with id -1 in the corresponding
						// table

typedef INT32 idbID;	// Integer-representation database ID's used for tables with small ID's as STATUS, RELEASE ...
						// used to avoid overhead in tables where never high number will be used
						// To signal an unknown id, the number -1 is used. This refers to the row with id -1 in the corresponding
						// table

            // set Calltype for functions
#define __PRODADLL_CALLTYPE__          __stdcall

#endif



//******************************************************************************
//******************************************************************************
// struct definitions
#if defined(__PRODADLL_EXPORT__) || defined(__PRODADLL_PASS_1__)


////////////////////////////////////////////////////////////////////////////////////////
// Language data handling

typedef struct LanguageData {
	idbID	id;				// Id of record
	char	isoCode[ PRODANGDLL_ISOCODE_SIZE ];	// Iso Code (en,de,…)
	char	name[ PRODANGDLL_LANGUAGEDATA_NAME_SIZE ];		// Descriptional name (English)
} * LanguageDataPtr;

////////////////////////////////////////////////////////////////////////////////////////
// Opaque data handling
// Preference key MAXBLOBSIZE (Numer of bytes) will be used to
// delimit the maximum size of binaries to store

typedef struct OpaqueData
{
	cdbID	id;				// Id of record
	idbID	mimeTypeId;		// Id of associated mime type
	int		binLength;		// Length of binary data
	void 	*binary;		// Pointer to binary data
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];// Translated description
} *OpaqueDataPtr;

typedef struct MimeType {
	idbID	id;					// Id of record
	char	mimeType[ PRODANGDLL_MIMETYPE_SIZE ];		// Mimetype (image/jpeg)
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *MimeTypePtr;

typedef struct UnitData {
	idbID	id;					// Id of record
	char	unitName[ PRODANGDLL_UNITNAME_SIZE ];		// Name of unit
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason of last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last changed by user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} * UnitDataPtr;

////////////////////////////////////////////////////////////////////////////////////////
// System handling

typedef struct Identification {
	idbID	processId;		// This process
	idbID	systemId;		// This system
	idbID	processStepId;	// The process step id
	idbID	wabcoPartId;	// The Wabco part id
}  *IdentificationPtr;



typedef struct System {
	idbID	id;			// Id of Record
	char	name[ PRODANGDLL_SYSTEM_NAME_SIZE ];	// Name of system
} *SystemPtr;

////////////////////////////////////////////////////////////////////////////////////////
// Process handling

typedef struct WabcoPart {
	idbID	id;					// Id of record
	idbID	workCenterId;		// Id of work center
	cdbID	contentId;			// Id of binary data
	cdbID	previewId;			// Id of preview for above binary
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason of last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last changed by user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	productName[ PRODANGDLL_PRODUCTNAME_SIZE ];	// Name of the product
	char	wabcoNumber[ PRODANGDLL_WABCONUMBER_SIZE ];	// The Wabco Number
} *WabcoPartPtr;


typedef struct Process {
	idbID	id;					// Id of record
	idbID	productionLineId;	// Id of production line
	idbID	releaseId;			// Id of release status
	cdbID	contentId;			// Id of binary data
	cdbID	previewId;			// Id of preview for binary
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason for last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last change by user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *ProcessPtr;


typedef struct ProcessStep {
	idbID	id;					// Id of record
	idbID	processId;			// Id of the process
	idbID	systemId;			// Id of the system record
	idbID	releaseId; 			// Id of release status
	int		processSequence;	// Process sequence number
	double	limitYellow;		// ‘Yellow’ warning level
	double	limitRed;			// ‘red’ warning level
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason of last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last change user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	filename[ PRODANGDLL_FILENAME_SIZE ];		// A Filename
	char	transfer[ PRODANGDLL_TRANSFER_SIZE ];		// Transfer
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *ProcessStepPtr;


typedef struct ProcessStepParam {
	idbID	id;					// Id of record
	idbID	processStepId;		// Id of process step record
	idbID	unitId;				// Id of unit record
	cdbID	contentId;			// Id of binary data
	cdbID	previewId;			// Id of preview for above binary
	double	value;				// The Value
	char	valueText[ PRODANGDLL_VALUETEXT_SIZE ];		// Additional value as text
	int		paramSequence;		// The parameter sequence number
	int		history;			// History flag
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason of last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last change user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *ProcessStepParamPtr;


typedef struct TestStep {
	idbID	id;					// Id of record
	idbID	processStepId;		// Id of process step record
	int		testSequence;		// Sequence or order
  int		testOrder;			// Sequence or order
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason of last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last change user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *TestStepPtr;

typedef struct TestStepParam {
	idbID	id;					// Id of record
	idbID	testStepId;			// Id of test step record
	idbID	unitId;				// Id of unit
	cdbID	contentId;			// Id of binary data
	cdbID	previewId;			// Id of preview for above binary
	double	value;				// The value
	char	valueText[ PRODANGDLL_VALUETEXT_SIZE ];		// Additional value as text
	int		paramSequence;		// The sequence number
	int		history;			// (Old) History flag
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason for last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last change user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date iof last change
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *TestStepParamPtr;

typedef struct TestValue {
	idbID	id;					// Id of record
	idbID	testStepId;			// Id of test step record
	idbID	releaseId;			// Id of release status
	idbID	unitId;				// Id of unit record
	cdbID	contentId;			// Id of binary data
	cdbID	previewId;			// Id of preview for above binary
	double	maximum;			// Maximum value
	double	minimum;			// Minimum value
	char	valueText[ PRODANGDLL_VALUETEXT_SIZE ];		// Additional value as text
	int		testValueSequence;	// Sequence of record
	int		history;			// (Old) history flag
	char	mdReason[ PRODANGDLL_MDREASON_SIZE ];		// Reason of last change
	char	mdUser[ PRODANGDLL_MDUSER_SIZE ];			// Last change user
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *TestValuePtr;

////////////////////////////////////////////////////////////////////////////////////////
// Product handling
// The related tables can use high numbered ID's so all structures contain cdbID types for their ID's

typedef struct Product {
	cdbID	id;					// Id of record
	idbID	wabcoPartId;		// Id of Wabco Part record
	char	serialNumber[ PRODANGDLL_SERIALNUMBER_SIZE ];	// Serial number
	char	comment[ PRODANGDLL_COMMENT_SIZE ];		// A comment
	int		individual;			// Individual flag
	idbID	crProcessStepId;	// Id of creating process step
	idbID	mdProcessStepId;	// Id of modifying process step
	char	crTime[ PRODANGDLL_CRTIME_SIZE ];			// Date of creation
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
} *ProductPtr;

typedef struct Product_lsn { // Product with long serial number
	cdbID	id;					// Id of record
	idbID	wabcoPartId;		// Id of Wabco Part record
	char	serialNumber[ PRODANGDLL_SERIALNUMBER_SIZE_LSN ];	// Serial number (Long Serial Number)
	char	comment[ PRODANGDLL_COMMENT_SIZE ];		// A comment
	int		individual;			// Individual flag
	idbID	crProcessStepId;	// Id of creating process step
	idbID	mdProcessStepId;	// Id of modifying process step
	char	crTime[ PRODANGDLL_CRTIME_SIZE ];			// Date of creation
	char	mdTime[ PRODANGDLL_MDTIME_SIZE ];			// Date of last change
} *Product_lsnPtr;


////////////////////////////////////////////////////////////////////////////////////////
// Result handling

typedef struct ProcessResult {
	cdbID	id;				// Id of record
	cdbID	productId;		// Id of product record
	idbID	processId;		// Id of process record
	idbID	statusId;		// The status
	char	startTime[ PRODANGDLL_STARTTIME_SIZE ];	// Start of process
	char	endTime[ PRODANGDLL_ENDTIME_SIZE ]; 	// End of process
} *ProcessResultPtr;


typedef struct ProcessStepResult {
	cdbID	id;					// Id fo record
	cdbID	processResultId;	// Id of process result
	idbID	processStepId;		// id of process step
	idbID	statusId;			// Status
	idbID	operatorId;			// Id of Operator (not a foreign key!)
	char	startTime[ PRODANGDLL_STARTTIME_SIZE ];		// Start of process step
	char	endTime[ PRODANGDLL_ENDTIME_SIZE ];		// End of process step
} *ProcessStepResultPtr;


typedef struct TestStepResult {
	cdbID	id;						// Id of record
	cdbID	processStepResultId;	// Id of process step result
	idbID	testStepId;				// Id of test step
	idbID	statusId;				// Status
} *TestStepResultPtr;


typedef struct TestValueResult {
	cdbID	id;					// Id of record
	cdbID	testStepResultId;	// Id of test step result
	idbID	testValueId;		// Id of test value
	double	result;				// Result value
	idbID	statusId;			// Status
	cdbID	contentId;			// Id of binary result
} *TestValueResultPtr;


typedef struct ProductionLine {
	idbID	id;					// Id of record
	char	description[ PRODANGDLL_DESCRIPTION_SIZE ];	// Translated description
} *ProductionLinePtr;

typedef struct Product_Component {
	Product_lsnPtr product;
	Product_lsnPtr component;
	ProcessStepResultPtr processStepResult;
	int qty;
	int level;
} *Product_ComponentPtr;


typedef struct Product_Component_wnr_snr {
	char	product_wabcoNumber[ PRODANGDLL_WABCONUMBER_SIZE ];		// Product WABCO Number
	char	product_serialNumber[ PRODANGDLL_SERIALNUMBER_SIZE_LSN ];	// Product Serial number
	char	component_wabcoNumber[ PRODANGDLL_WABCONUMBER_SIZE ];	// Component WABCO Number
	char	component_serialNumber[ PRODANGDLL_SERIALNUMBER_SIZE_LSN ];	// Component Serial number
	cdbID	processStepResultId;									// process_step_result.id
	int qty;
	int level;

} *Product_Component_wnr_snrPtr;

// end of struct definitions
#endif // !defined(__PRODADLL_EXPORT__) || defined(__PRODADLL_PASS_1__)


//******************************************************************************
//******************************************************************************
// preparations for function definitions

#if defined(__PRODADLL_EXPORT__)

#define DllEXPORT             __declspec( dllexport )
#define __FUNCTYPE_1__        extern "C" DllEXPORT
#define __FUNCTYPE_2__( _a )  __PRODADLL_CALLTYPE__ _a
#define __NAMESPACE__( _a )   _a

#elif defined(__PRODADLL_IMPORT__)

#define DllIMPORT             __declspec( dllexport )
#define __FUNCTYPE_1__        extern "C" DllIMPORT
#define __FUNCTYPE_2__( _a )  __PRODADLL_CALLTYPE__ _a
#define __NAMESPACE__( _a )   _a

#elif defined(__PRODADLL_PASS_2__)

#if !defined(__FUNCTYPE_1__) || !defined(__FUNCTYPE_2__) || !defined(__NAMESPACE__)
#error #defines not generated correctly (example in following comment)
// #define __FUNCTYPE_1__
// #define __FUNCTYPE_2__( _a )  ( __PRODADLL_CALLTYPE__ *P##_a )
// #define __NAMESPACE__( _a )   ProdaNG_DLL::##_a
#endif

#endif //  #if defined(__PRODADLL_PASS_2__)
#endif //  #if defined(__PRODADLL_EXPORT__)

//******************************************************************************
//******************************************************************************
// function definitions
#if defined(__PRODADLL_EXPORT__) || defined(__PRODADLL_IMPORT__) || defined(__PRODADLL_PASS_2__)

// InitProDll
// IN
//  numContexts
//
// Has to be called in Main Thread before any other DLL function can be used.
// Parameter defines how many independend context the DLL will provide.
// Each simultanious Login() creates a session and requires one context:
//   0: There will be only one context used. Repititive Login()s always closes
//	    the current session and creates a new session.
//  >0: DLL initialises the given number of contexts and therefore allows
//      the same number of Login()s in parallel.
//
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( InitProDll ) ( int numContexts );


//  ExitProDll
//
//  Closes all Database connections, frees the contexts and other resources.
//  InitProDll must be called again to make use of the DLL.
//
__FUNCTYPE_1__ void __FUNCTYPE_2__( ExitProDll ) ( void );


// Login
// IN
//	user
//	password
//	database (Service name / SID)
// OUT
//	handle
//
// Logon to database returning a handle to the db context
//

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( Login )( char*     user,
                                               char*     password,
                                               char*     database,
                                               dbHandle* handle );

// SetPreference
// IN
//	handle
//  key			Name of preference to set
//  value		New value of preference
//
// Set one of the preferences named
// RETRYCOUNT		(Number >= 0)
// RETRYWAIT		(Number >= 0 Seconds)
// RETRYISRECONNECT (Number False = 0, True != 0 )
//

__FUNCTYPE_1__  RetVal __FUNCTYPE_2__( SetPreference )( dbHandle handle, char* key, int value );

// Logout
// IN
//	handle
//
// Logoff from database freeing the handle an its resources
//

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( Logout )( dbHandle handle );

// SetDBId
// IN
//	handle
//  dbId				Database Id
//
// Overwrite the default DBId from preference DBID (Number) for the current session

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetDBId )( dbHandle handle,
                                                 idbID    dbId );

// FreeData
// IN
// 	data   pointer to allocated data
//
// function is required because of different memory management

__FUNCTYPE_1__ void __FUNCTYPE_2__( FreeData )( void **data );

// FreeStructArray
// IN
// 	arrayOfPtrs		Array of structure pointers returned by several functions
//
// All returned structure arrays can be freed using this function

__FUNCTYPE_1__ void __FUNCTYPE_2__( FreeStructArray )( void **arrayOfPtrs );

// GetLastErrorMsg
// IN
// 	handle
//
// Returns the last error message caused by an ORACLE Error
// This text points to static area in the handle and will be overriden
// by the next call to a DLL function.

__FUNCTYPE_1__ char * __FUNCTYPE_2__( GetLastErrorMsg )( dbHandle handle );


// GetDatabaseTime
// IN
// 	handle
//
// OUT
//	timeBuf	A character array sized at least 24 chars to hold the returned system time
//
// Queries the database for the actual date and time

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetDatabaseTime )( dbHandle handle,
                                                         char     timeBuf[24] );

////////////////////////////////////////////////////////////////////////////////////////
// Language data handling
// GetLanguages
// IN
//	handle
// OUT
//	languages		Array of LanguageDataPtr( alloc by callee, use FreeStructArray() to free)
//	countPtr		Size of above array
//
// Returns all languages known to db as array (ordered alphabetical) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetLanguages )( dbHandle handle,
                                                      __NAMESPACE__( LanguageDataPtr ) **languages,
                                                      int*     countPtr );

// SetLanguage
// IN
//	handle
//  languageId		Id of language
//
// Set current language for this application while running
// All label translations(in and out) will be according to this language
// Additional error code:
// ERROR_NO_DATA in case the language id passed is not present in the database

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetLanguage )( dbHandle handle,
                                                     idbID    languageId );



////////////////////////////////////////////////////////////////////////////////////////
// Opaque data handling
// Preference key MAXBLOBSIZE (Numer of bytes) will be used to
// delimit the maximum size of binaries to store

// GetOpaqueData
// IN
//	handle
//  opaqueId		Id of record
//
// OUT
//	opaqueData		Record (alloc and free by caller)
//
// Get record from OpaqueData table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetOpaqueData )( dbHandle handle,
                                                       cdbID    opaqueId,
                                                       __NAMESPACE__( OpaqueDataPtr ) opaqueData );

// NewOpaqueData
// IN
//	handle
//  opaqueData		New record content (alloc and free by caller)
//
// Create a new opaque data record, Updated fields in opaqueData on return.
// ERROR_MORE_DATA returned in case MAXBLOBSIZE is exceeded.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewOpaqueData )( dbHandle handle,
                                                       __NAMESPACE__( OpaqueDataPtr ) opaqueData );

// SetOpaqueData
// IN
//	handle
//  opaqueData		Record to update (alloc and free by caller)
//
// Update an existing opaque data record
// ERROR_MORE_DATA returned in case MAXBLOBSIZE is exceeded.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetOpaqueData )( dbHandle handle,
                                                       __NAMESPACE__( OpaqueDataPtr ) opaqueData );

// DeleteOpaqueData
// IN
//	handle
//  opaqueId		Id of record to delete
//
// Deletes an existing opaque data record identified by its ID

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteOpaqueData )( dbHandle handle,
                                                          cdbID opaqueId );

// GetOpaqueDataResult
// IN
//	handle
//  opaqueId		Id of record
//
// OUT
//	opaqueData		Record (alloc and free by caller)
//
// Get record from OpaqueDataResult table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetOpaqueDataResult )( dbHandle handle,
                                                       cdbID    opaqueId,
                                                       __NAMESPACE__( OpaqueDataPtr ) opaqueData );

// NewOpaqueDataResult
// IN
//	handle
//  opaqueData		New record content (alloc and free by caller)
//
// Create a new opaque data result record, Updated fields in opaqueData on return.
// ERROR_MORE_DATA returned in case MAXBLOBSIZE is exceeded.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewOpaqueDataResult )( dbHandle handle,
                                                       __NAMESPACE__( OpaqueDataPtr ) opaqueData );

// SetOpaqueDataResult
// IN
//	handle
//  opaqueData		Record to update (alloc and free by caller)
//
// Update an existing opaque data result record
// ERROR_MORE_DATA returned in case MAXBLOBSIZE is exceeded.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetOpaqueDataResult )( dbHandle handle,
                                                       __NAMESPACE__( OpaqueDataPtr ) opaqueData );

// DeleteOpaqueDataResult
// IN
//	handle
//  opaqueId		Id of record to delete
//
// Deletes an existing opaque data record reaslt identified by its ID

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteOpaqueDataResult )( dbHandle handle,
                                                          cdbID opaqueId );


// GetMimeTypes
// IN
//	handle
// OUT
//	mimeTypes		Array of MimeTypePtr (alloc by callee, use FreeStructArray() to free)
//	countPtr		Size of above array
//
// Returns all mimetypes known to db as array (ordered alphabetical) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetMimeTypes )( dbHandle  handle,
                                                      __NAMESPACE__( MimeTypePtr ) **mimeTypes,
                                                      int*      countPtr );
// GetUnits
// IN
//	handle
// OUT
//	units		Array of UnitDataPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all units known to db as array (ordered by name) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetUnits )( dbHandle handle,
                                                  __NAMESPACE__( UnitDataPtr ) **units,
                                                  int*     countPtr);



////////////////////////////////////////////////////////////////////////////////////////
// System handling

// IdentifyMe
// IN
//	handle
//	systemName			Name of this system
//	wabcoNumber			Wabco number produced by this system
//	processSequence		Process sequence number of this system (specify 0 as Optional)
//	processId			Process id of this system (specify 0 as Optional)
// OUT
//	myIdent				Record identifying this system (alloc and free by caller)
//
// Identifies this system from given input parameters and returns an ident record
// ERROR_NO_DATA is returned if insufficient data supplied or ERROR_MORE_DATA if the system could not
// be uniquely identified.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( IdentifyMe )( dbHandle handle,
                                                    char*    systemName,
                                                    char*    wabcoNumber,
			                                              int      processSequence,
                                                    idbID    processId,
                                                    __NAMESPACE__( IdentificationPtr ) myIdent );

// GetSystem
// IN
//	handle
//  systemId	Id of system
//
// OUT
//	system		Record (alloc and free by caller)
//
// Get record from system table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetSystem )( dbHandle handle,
                                                   idbID    systemId,
                                                   __NAMESPACE__( SystemPtr ) system );


// startIdleTime
// IN
//	handle
//  systemId		Id of system
//  idleReasonId	Reason of idle time
//	comment			Comment
//
// Marks start of idle phase

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( StartIdleTime )( dbHandle handle,
                                                       idbID    systemId,
                                                       idbID    idleReasonId,
                                                       char*    comment );

// endIdleTime
// IN
//	handle
//  systemId	Id of system
//
// Marks end of idle phase - this completes the last idletime record created
// by startIdleTime()

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( EndIdleTime )( dbHandle handle,
                                                     idbID    systemId );


// GetSystems
// IN
//	handle
// OUT
//	systems		Array of SystemPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all systems known to db as array (ordered alphabetical) of structure pointers
// and the size of the array
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetSystems )( dbHandle handle,
                                                    __NAMESPACE__( SystemPtr ) **systems,
                                                    int*     countPtr );

/////////////////////////////////////////////////////////////////////////////////////
// UpdateWabcoNumber
// IN
//	handle
//	WabcoNumber is a “old” WABCO number which we want to change.
//	serialNumber is a serial number for product for which we want to change WABCO number.
//	newWabcoNumber is a “new” WABCO number
//
// Updates WABCO number for given product (identified by WabcoNumber and serialNumber), set newWabcoNumber
//
// Returns the standard error codes 

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( UpdateWabcoNumber )( dbHandle handle, char *WabcoNumber, char *SerialNumber, char *newWabcoNumber );



/////////////////////////////////////////////////////////////////////////////////////
// GetProductionLine
// IN
//  handle
//  productionLineID		Id of productionLine
//
// OUT
//	productionLine		Record (alloc and free by caller)
//
// Get record from productionLine table 
//
// Returns the standard error codes

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProductionLine )( dbHandle handle, 
                                      idbID ProductionLineId, 
                                      __NAMESPACE__( ProductionLinePtr ) productionline );

/////////////////////////////////////////////////////////////////////////////////////
// GetProductionLines
// IN
//	Handle
// OUT
//	productionlines	Array of ProductionLinePtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all productionlines known to db as array (ordered by id) of structure pointers 
// and the size of the array
//
// Returns the standard error codes

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProductionLines )( dbHandle handle, 
                                      __NAMESPACE__( ProductionLinePtr ) **productionlines, 
                                      int *countPtr);

////////////////////////////////////////////////////////////////////////////////////////
// Process handling

// GetWabcoPart
// IN
//	handle
//  wabcoPartId	Id of wabco part
//
// OUT
//	wabcoPart		Record (alloc and free by caller)
//
// Get record from wabcopart table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetWabcoPart )( dbHandle handle,
                                                      idbID    wabcoPartId,
                                                      __NAMESPACE__( WabcoPartPtr ) wabcoPart );

// GetWabcoPart_wabcoNumber
// IN
//	handle
//  wabcoNumber	is WABCO number
//
// OUT
//	wabcoPart		Record (alloc and free by caller)
//
// Get record from wabcopart table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetWabcoPart_wabcoNumber )( dbHandle handle,
                                                      char*    wabcoNumber,
                                                      __NAMESPACE__( WabcoPartPtr ) wabcoPart );

// GetWabcoParts
// IN
//	handle
// OUT
//	wabcoParts	Array of WabcoPartPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all WABCO parts known to db as array (ordered alphabetical) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetWabcoParts )( dbHandle handle,
                                                       __NAMESPACE__( WabcoPartPtr ) **wabcoParts,
                                                       int*     countPtr );

// NewWabcoPart
// IN
//	handle
//
// OUT
//	wabcoPart		Record (alloc and free by caller)
//
// Get record from wabcopart table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewWabcoPart )( dbHandle handle,
                                                      __NAMESPACE__( WabcoPartPtr ) wabcoPart );

// NewWabcoPart_Process
// IN
//	handle
//	processId
//	wabcoPartId
//
// Connect Process to Wabcopart

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewWabcoPart_Process )( dbHandle handle,
                                                      idbID wabcoPartId, idbID processId);

// GetProcess
// IN
//	handle
//  processId		Id of process
//
// OUT
//	process			Record (alloc and free by caller)
//
// Get record from process table
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcess )( dbHandle handle,
                                                    idbID    processId,
                                                    __NAMESPACE__( ProcessPtr ) process );



// GetProcesses
// IN
//	handle
// OUT
//	processes	Array of ProcessPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all processes known to db as array (ordered by id) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcesses )( dbHandle handle,
                                                      __NAMESPACE__( ProcessPtr ) **processes,
                                                      int*     countPtr );


// GetWabcoPartProcesses
// IN
//	handle
//  wabcoPartId	Id of Wabco Part
// OUT
//	processes	Array of ProcessPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all processes known for the given Wabco Part ID as array (ordered by id) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetWabcoPartProcesses )( dbHandle handle,
                                                               idbID    wabcoPartId,
                                                               __NAMESPACE__( ProcessPtr ) **processes,
                                                               int*     countPtr );


// GetProcessStep
// IN
//	handle
//  processStepId	Id of process step
//
// OUT
//	processStep		Record (alloc and free by caller)
//
// Get record from process step table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcessStep )( dbHandle handle,
                                                        idbID    processStepId,
                                                        __NAMESPACE__( ProcessStepPtr ) processStep );


// GetProcessSteps
// IN
//	handle
//  processId		Id of process
// OUT
//	processSteps	Array of ProcessStepPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr		Size of above array
//
// Returns all process steps for this process as array (ordered by sequence) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcessSteps )( dbHandle handle,
                                                         idbID    processId,
                                                         __NAMESPACE__( ProcessStepPtr ) **processSteps,
                                                         int*     countPtr );
/*
// NewProcessStep
// IN
//	handle
//	processStep		Record (alloc and free by caller)
//
// OUT
//	processStep		Record (alloc and free by caller)
//
// Get record from process step table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewProcessStep )( dbHandle handle,
                                                        __NAMESPACE__( ProcessStepPtr ) processStep );

// SetProcessStep
// IN
//	handle
//	processStep		Record (alloc and free by caller)
//
// OUT
//	processStep		Record (alloc and free by caller)
//
// Get record from process step table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetProcessStep )( dbHandle handle,
                                                        __NAMESPACE__( ProcessStepPtr ) processStep );

// DeleteProcessStep
// IN
//	handle
//	processStep		Record (alloc and free by caller)
//
// OUT
//	processStep		Record (alloc and free by caller)
//
// Get record from process step table

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteProcessStep )( dbHandle handle,
                                                        __NAMESPACE__( ProcessStepPtr ) processStep );
*/
// GetProcessStepParams
// IN
//	handle
//  processStepID		Id of process step
// OUT
//	processStepParams	Array of ProcessStepPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr			Size of above array
//
// Returns all process step parameters for this process step as array (ordered by sequence) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcessStepParams )( dbHandle handle,
                                                              idbID    processStepId,
                                                              __NAMESPACE__( ProcessStepParamPtr ) **processStepParams,
                                                              int*     countPtr );

// NewProcessStepParam
// IN
//	handle
//	processStepParams	ProcessStepPtr
//
//OUT
//	processStepParams	ProcessStepPtr
//
// Creates new Process Step Parameter

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewProcessStepParam )( dbHandle handle,
                                                              __NAMESPACE__( ProcessStepParamPtr ) processStepParam);

// SetProcessStepParam
// IN
//	handle
//	processStepParams	ProcessStepPtr
//
// Changes Process Step Parameter

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetProcessStepParam )( dbHandle handle,
                                                              __NAMESPACE__( ProcessStepParamPtr ) processStepParam);

// DeleteProcessStepParam
// IN
//	handle
//	processStepParams	ProcessStepPtr
//
// Changes Process Step Parameter

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteProcessStepParam )( dbHandle handle,
                                                              idbID processStepParamId);


// GetTestSteps
// IN
//	handle
//  processStepID		Id of process step
// OUT
//	testSteps			Array of TestStepPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr			Size of above array
//
// Returns all test steps for this process step as array (ordered by sequence) of structure pointers
// and the size of the array
// when you will change this function please remember to change also GetTestSteps_orderby

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetTestSteps )( dbHandle handle,
                                                      idbID    processStepId,
                                                      __NAMESPACE__( TestStepPtr ) **testSteps,
                                                      int*     countPtr );



/////////////////////////////////////////////////////////////////////////////////////
// GetTestSteps_orderby
// IN
//	handle
//  processStepID		Id of process step
// OUT
//	testSteps			Array of TestStepPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr			Size of above array
//  orderby				sort order, allowed values: GETTESTSTEPS_ORDERBY_TEST_SEQUENCE, GETTESTSTEPS_ORDERBY_TEST_ORDER
//
// Returns all test steps for this process step as array of structure pointers 
// and the size of the array
//
// Returns the standard error codes and ERROR_INVALID_PARAMETER when "orderby" is not any of above allowed values
// when you will change this function please remember to change also GetTestSteps

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetTestSteps_orderby )( dbHandle handle,
                                                      idbID    processStepId,
                                                      __NAMESPACE__( TestStepPtr ) **testSteps,
                                                      int*     countPtr,
													  int orderby );



// NewTestStep
// IN
//	handle
//	testStep			TestStepPtr
//  releaseId
// OUT
//	testStep			TestStepPtr
//	countPtr			Size of above array
//
// Returns all test steps for this process step as array (ordered by sequence) of structure pointers
// and the size of the array
// when you will change this function please remember to change also GetTestSteps_orderby

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewTestStep )( dbHandle handle,
                                                      __NAMESPACE__( TestStepPtr ) testStep, int releaseId);


// SetTestStep
// IN
//	handle
//	testStep			TestStepPtr
// OUT
//	testStep			TestStepPtr
//	countPtr			Size of above array
//
// Returns all test steps for this process step as array (ordered by sequence) of structure pointers
// and the size of the array
// when you will change this function please remember to change also GetTestSteps_orderby

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetTestStep )( dbHandle handle,
                                                      __NAMESPACE__( TestStepPtr ) testStep, int releaseId);

// DeleteTestStep
// IN
//	handle
//	testStep			TestStepPtr
// OUT
//	testStep			TestStepPtr
//	countPtr			Size of above array
//
// Returns all test steps for this process step as array (ordered by sequence) of structure pointers
// and the size of the array
// when you will change this function please remember to change also GetTestSteps_orderby

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteTestStep )( dbHandle handle,
                                                      idbID testStepId);

// GetTestStepParams
// IN
//	handle
//  testStepId			Id of test step
// OUT
//	testStepParams		Array of TestStepParamPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr			Size of above array
//
// Returns all test step parameters for this test step as array (ordered by sequence) of structure pointers
// and the size of the array

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetTestStepParams )( dbHandle handle,
                                                           idbID    testStepId,
                                                           __NAMESPACE__( TestStepParamPtr ) **testStepParams,
                                                           int*     countPtr );


// NewProcessStepParam
// IN
//	handle
//	processStepParams	ProcessStepPtr
//
// Creates new Process Step Parameter

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewTestStepParam )( dbHandle handle,
                                                              __NAMESPACE__( TestStepParamPtr ) testStepParam, int do_commit=1);

// SetProcessStepParam
// IN
//	handle
//	processStepParams	ProcessStepPtr
//
// Changes Process Step Parameter

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetTestStepParam )( dbHandle handle,
                                                              __NAMESPACE__( TestStepParamPtr ) testStepParam);

// DeleteProcessStepParam
// IN
//	handle
//	processStepParams	ProcessStepPtr
//
// Changes Process Step Parameter

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteTestStepParam )( dbHandle handle,
                                                              idbID testStepParamId);




// GetTestValues
// IN
//	handle
//  testStepId		Id of test step
// OUT
//	testValues		Array of TestStepParamPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr		Size of above array
//
// Returns all test values for this test step as array (ordered by sequence) of structure pointers
// and the size of the array
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetTestValues )( dbHandle handle,
                                                       idbID    testStepId,
                                                       __NAMESPACE__( TestValuePtr ) **testValues,
                                                       int*     countPtr );


// NewTestValue
// IN
//	handle
//  testValue		Test value record to add (alloc and free by caller)
//
// Create a test value record with new values and mark the origin record as not-in-use-anymore

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewTestValue )( dbHandle handle,
                                                      __NAMESPACE__( TestValuePtr ) testValue, int do_commit=1);


// SetTestValue
// IN
//	handle
//  testValue		Test value record to update (alloc and free by caller)
//
// Create a test value record with new values and mark the origin record as not-in-use-anymore

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetTestValue )( dbHandle handle,
                                                      __NAMESPACE__( TestValuePtr ) testValue );


// DeleteTestValue
// IN
//	handle
//  testValue		Test value record to update (alloc and free by caller)
//
// Create a test value record with new values and mark the origin record as not-in-use-anymore

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( DeleteTestValue )( dbHandle handle,
                                                      idbID testValueId );


////////////////////////////////////////////////////////////////////////////////////////
// Product handling
// The related tables can use high numbered ID's so all structures contain cdbID types for their ID's

// NewProduct
// IN
//	handle
//  product		Product record filled with base data (alloc and free by caller)
//
// Create a new product record in db. Fields will be updated on return
// In case product exists, ERROR_MORE_DATA is returned.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewProduct )( dbHandle handle,
                                                    __NAMESPACE__( ProductPtr ) product );

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewProduct_lsn )( dbHandle handle,
                                                    __NAMESPACE__( Product_lsnPtr ) product );

// GetProduct
// IN
//	handle
//  wabcoPartId		Wabco part id to search
//  serialNumber	Serial number to search
// OUT
//  product			Product record found (alloc and free by caller)
//
// Get product record identified by the wabcoPartId and the serial number

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct )( dbHandle handle,
                                                    idbID    wabcoPartId,
                                                    char*    serialNumber,
                                                    __NAMESPACE__( ProductPtr ) product );

// GetProduct with Long Serial Number
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct_lsn )( dbHandle handle,
                                                    idbID    wabcoPartId,
                                                    char*    serialNumber,
                                                    __NAMESPACE__( Product_lsnPtr ) product );

// GetProduct_serialNumber
// IN
//	handle
//  serialNumber	Serial number to search
// OUT
//  product			Product record found (alloc and free by caller)
//
// Get product record identified by the wabcoPartId and the serial number

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct_serialNumber )( dbHandle handle,
                                                    char*    serialNumber,
                                                    __NAMESPACE__( Product_lsnPtr ) product );

// GetProduct_productId
// IN
//	handle
//  productId	product.id
// OUT
//  product			Product record found (alloc and free by caller)
//
// Get product record identified by the wabcoPartId and the serial number

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct_productId )( dbHandle handle,
                                                    char*    productId,
                                                    __NAMESPACE__( Product_lsnPtr ) product );

// GetProduct_wabcoNumber_serialNumber
// IN
//	handle
//  wabcoPartId		Wabco part id to search
//  serialNumber	Serial number to search
// OUT
//  product			Product record found (alloc and free by caller)
//
// Get product record identified by the wabcoPartId and the serial number

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct_wabcoNumber_serialNumber )( dbHandle handle,
                                                    char*    wabcoNumber,
                                                    char*    serialNumber,
                                                    __NAMESPACE__( Product_lsnPtr ) product );

// SetProduct
// IN
//	handle
//  product			Product record to update (alloc and free by caller)
//
// Update the product record with new values.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetProduct )( dbHandle handle,
                                                    __NAMESPACE__( ProductPtr ) product );

// for Long Serial number
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetProduct_lsn )( dbHandle handle,
                                                    __NAMESPACE__( Product_lsnPtr ) product );

// GetNewestProduct
// IN
//	handle
//  wabcoPartId		Wabco part id of product
// OUT
//  product			Product record found (has to be allocated by caller)
//	statusPtr		Status of query (used as in old DLL)
//
// Get newest product record identified by the wabcoPartId

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetNewestProduct )( dbHandle handle,
                                                          idbID    WabcoPartId,
                                                          __NAMESPACE__( ProductPtr ) product,
                                                          int*     statusPtr );

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetNewestProduct_lsn )( dbHandle handle,
                                                          idbID    WabcoPartId,
                                                          __NAMESPACE__( Product_lsnPtr ) product,
                                                          int*     statusPtr );

// GetNextSerialNumber
// IN
//	handle
//  wabcoPartId		Wabco part id of product
// OUT
//  serialNumber	Next serial number to use (has to be allocated by caller)
//	statusPtr		Status of query (used as in old DLL)
//
// Get next serial number for a product identified by the wabcoPartId.
// Only numeric serial numbers can be generated

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetNextSerialNumber )( dbHandle handle,
                                                             idbID    WabcoPartId,
                                                             char*     serialNumber,
                                                             int*     statusPtr );

// AddComponent
// IN
//	handle
//  product_component - structure with product, component, processstepresult and qty. lavel is not used
//
// Create a new product record in db. Fields will be updated on return
// In case product exists, ERROR_MORE_DATA is returned.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( AddComponent )( dbHandle handle,
                                                    __NAMESPACE__( Product_ComponentPtr ) product_component );

// AddComponent
// IN
//	handle
//  product_wabcoNumber, product_serialNumber - to identify product
//  component_wabcoNumber, component_serialNumber - to identify component for product
//
// Create a new product record in db. Fields will be updated on return
// In case product exists, ERROR_MORE_DATA is returned.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( AddComponent_wabcoNumber_serialNumber )( dbHandle handle,
                                                    char*    product_wabcoNumber,
                                                    char*    product_serialNumber,
                                                    char*    component_wabcoNumber,
                                                    char*    component_serialNumber,
													char*	 processStepResultId,
													int qty);

// GetProduct_ComponentList
// IN
//	handle
//  product_component pointer to table of pointers with of product_component structure
//
// Create a new product record in db. Fields will be updated on return
// In case product exists, ERROR_MORE_DATA is returned.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct_ComponentList )( dbHandle handle,
                                                    __NAMESPACE__( Product_ComponentPtr ) **product_component,
													int*     countPtr );

// GetProduct_ComponentList
// IN
//	handle
//  product_component_wnr_snr pointer to table of pointers with of Product_Component_wnr_snrPtr structure
//
// Create a new product record in db. Fields will be updated on return
// In case product exists, ERROR_MORE_DATA is returned.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProduct_ComponentList_wnr_snr )( dbHandle handle,
                                                    char*    wabcoNumber,
                                                    char*    serialNumber,
                                                    __NAMESPACE__( Product_Component_wnr_snrPtr ) **product_component_wnr_snr,
													int*     countPtr );

// FreeProduct_ComponentList
// IN
//	handle
//  product_component - table of pointers with of product_component structure
//
// Create a new product record in db. Fields will be updated on return
// In case product exists, ERROR_MORE_DATA is returned.

__FUNCTYPE_1__ void __FUNCTYPE_2__( FreeProduct_ComponentList )(__NAMESPACE__( Product_ComponentPtr ) *product_component_tbl_Ptr);


////////////////////////////////////////////////////////////////////////////////////////
// Result handling
// The result handling functions are used in a chain.
// 1. New records are created by using the New...() functions.
// 2. Test value results are set and checked.
// 3. Test step results are set and checked, including the test value results.
// 4. Process step results are set and checked, including the test step results.
// 5. Process results are set and checked including the process step result. This completes the chain.

// NewProcessResult
// IN
//	handle
//  processResult		Process result record filled with base data (alloc and free by caller)
//
// Create a new process result record in db. Fields will be updated on return

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewProcessResult )( dbHandle handle,
                                                          __NAMESPACE__( ProcessResultPtr ) processResult );

// GetProcessResult
// IN
//	handle
//  productId		Product id to search
//  processId		Process id to search
// OUT
//  processResult	Process result record found (alloc and free by caller)
//
// Get process result record identified by the productId and processId

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcessResult )( dbHandle handle,
                                                          cdbID    productId,
                                                          idbID    processId,
                                                          __NAMESPACE__( ProcessResultPtr ) processResult );

// SetProcessResult
// IN
//	handle
//  processResult	Process result record to update (alloc and free by caller)
//
// Update the process result record with new values. Apply checks accoring statusId setting.
// This call is the last in result chain after SetTestValueResult, SetTestStepResult and
// SetProcessStepResult.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetProcessResult )( dbHandle handle,
                                                          __NAMESPACE__( ProcessResultPtr ) processResult );


// NewProcessStepResult
// IN
//	handle
//  processStepResult		Process step result record filled with base data (alloc and free by caller)
//
// Create a new process setp result record in db. Fields will be updated on return

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewProcessStepResult )( dbHandle handle,
                                                              __NAMESPACE__( ProcessStepResultPtr ) processStepResult );

// GetProcessStepResult
// IN
//	handle
//  processResultId		Process result id to search
//  processStepId		Process step id to search
// OUT
//  processStepResult	Process step result record found (alloc and free by caller)
//
// Get process step result record identified by the processResultId and processStepId

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcessStepResult )( dbHandle handle,
                                                              cdbID    processResultId,
                                                              idbID    processStepId,
                                                              __NAMESPACE__( ProcessStepResultPtr ) processStepResult );

// GetProcessStepResults
// IN
//	handle
//  processResultId	Id of process result record
// OUT
//	processStepResults	Array of ProcessStepResultPtr (alloc by callee, use FreeStructArray() to free)
//	countPtr	Size of above array
//
// Returns all process step result for a given process result id
// as array of structure pointers and the size of the array
//
// Returns the standard error codes

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetProcessStepResults )( dbHandle handle,
                                                               cdbID    processResultId,
									                            __NAMESPACE__( ProcessStepResultPtr ) **processStepResults,
                                                               int*     countPtr );

// GetPreviousProcessStepStatus
// IN
//	handle
//  processResultId	Id of process result record
//  processStepId	Id of process step record
//  strictlyMode	Check strict chronolical order
// OUT
//	processStepResult	ProcessStepResult record of the previous process step
//	statusPtr			Status of the matched record
//						-4   Found a result but there exists steps below with newer end time (reported only in strict mode)
//						-3   Found a result but is not the previous step (reported only in strict mode)
//						-2	 No according result found
//						-1	 No data found
//						>= 0 Status of the matched previous record
//
// Returns the previous process step result and stati. 
//
// Returns the standard error codes

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetPreviousProcessStepStatus )( dbHandle handle,
																	  cdbID		processResultId,
																	  idbID		processStepId,
																	  int		strictlyMode,
																	  __NAMESPACE__( ProcessStepResultPtr ) processStepResult,
																	  int*		statusPtr );

// SetProcessStepResult
// IN
//	handle
//  isRepeat					This step has been repeated
//  processStepResult			Product record to update (alloc and free by caller)
//
// Update the process step result record with new values. Apply checks accoring statusId setting.
// This call is the third in result chain after SetTestValueResult and SetTestStepResult.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetProcessStepResult )( dbHandle handle,
                                                              int      isRepeat,
                                                              __NAMESPACE__( ProcessStepResultPtr ) processStepResult );


// NewTestStepResult
// IN
//	handle
//  testStepResult		Test step result record filled with base data (alloc and free by caller)
//
// Create a new test step result record in db. Fields will be updated on return

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewTestStepResult )( dbHandle handle,
                                                          __NAMESPACE__( TestStepResultPtr ) testStepResult );

// GetTestStepResult
// IN
//	handle
//  processStepResultId		Process step result id to search
//  testStepId				Test step id to search
// OUT
//  testStepResult			Test step result record found (alloc and free by caller)
//
// Get test step result record identified by the processStepResultId and testStepId

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetTestStepResult )( dbHandle handle,
                                                           cdbID    processStepResultId,
                                                           idbID    testStepId,
                                                           __NAMESPACE__( TestStepResultPtr ) testStepResult );


// SetTestStepResult
// IN
//	handle
//  isRepeat				This step has been repeated
//  testStepResult			Test step result record to update (alloc and free by caller)
//
// Update the test step result record with new values. Apply checks according statusId setting.
// This call is the second in result chain after SetTestValueResult.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetTestStepResult )( dbHandle handle,
                                                           int      isRepeat,
                                                           __NAMESPACE__( TestStepResultPtr ) testStepResult );


// NewTestValueResult
// IN
//	handle
//  testValueResult		Test value result record filled with base data (alloc and free by caller)
//
// Create a new test value result record in db. Fields will be updated on return

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( NewTestValueResult )( dbHandle handle,
                                                            __NAMESPACE__( TestValueResultPtr ) testValueResult );

// GetTestValueResult
// IN
//	handle
//  testStepResultId		Test step result id to search
//  testValueId				Test value id to search
// OUT
//  testValueResult			Test value result record found (alloc and free by caller)
//
// Get test value result record identified by the testStepResultId and testValueId

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( GetTestValueResult )( dbHandle handle,
                                                            cdbID    testStepResultId,
                                                            idbID    testValueId,
                                                            __NAMESPACE__( TestValueResultPtr ) testValueResult );


// SetTestValueResult
// IN
//	handle
//  isRepeat				The test has been repeated
//  testValueResult			Test value result record to update (alloc and free by caller)
//
// Update the test value result record with new values. Apply checks according statusId setting.
// This call is the first in result chain.

__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( SetTestValueResult )( dbHandle handle,
                                                            int      isRepeat,
                                                            __NAMESPACE__( TestValueResultPtr ) testValueResult );


// WPL EAPU dedicated functions
__FUNCTYPE_1__ RetVal __FUNCTYPE_2__( eapu_check_ecusn )( dbHandle handle,
															 char*		wabcoNumber,
															 int		testSequence_hi,
															 int		testSequence_lo,
															 int		testValueSequence_hi,
															 int		testValueSequence_lo,
															 int		check_period,
															 char*		ecusn,
                                                             char*		serialNumber);

#endif

#undef  __FUNCTYPE_1__
#undef  __FUNCTYPE_2__
#undef  __NAMESPACE__
#if defined(__PRODADLL_EXPORT__)
#undef __PRODADLL_EXPORT__

#endif

