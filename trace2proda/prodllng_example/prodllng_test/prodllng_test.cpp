#define	_CRT_SECURE_NO_DEPRECATE 

#include <windows.h>
#include <stdio.h>
#include "../prodllng/ProdaNG_DLL.h"

int main()
{
/*
Please remember to set:
Struct Member Alignment to 1 Byte (/Zp1)
https://msdn.microsoft.com/en-us/library/xh3e3fd0.aspx

In Visual studio you will find this setting in:
Properties -> C/C++ -> Code Generation
*/
	
	RetVal	r; // return value from prodllng.dll functions
	dbHandle h1; // database handle
	char db_user[100]; // database user
	char db_pass[100]; // database password
	char db_name[100]; // database name
	idbID language_id; // language id
	char wabco_number[PRODANGDLL_WABCONUMBER_SIZE]; // WABCO number
	char system_name[PRODANGDLL_SYSTEM_NAME_SIZE]; // system name
	char serial_number[PRODANGDLL_SERIALNUMBER_SIZE_LSN]; // serial number

	char component_wabco_number[PRODANGDLL_WABCONUMBER_SIZE]; // component WABCO number
	char component_serial_number[PRODANGDLL_SERIALNUMBER_SIZE_LSN]; // component serial number


// values which should be in configuration file
	strcpy(db_user,"lcptb"); // database user - should be in configuration file
	strcpy(db_pass,"lcptb"); // database password - should be in configuration file
	strcpy(db_name,"proda_wpl_dev"); // database name - should be in configuration file
	language_id = 3; // language id  - should be in configuration file; 3=Polish, 2=English, 1=German; You can download list of languages using function GetLanguages

// values set in the process (ex. by employee on control panel) or configuration file
	strcpy(wabco_number,"0000000111"); // product WABCO number
	strcpy(system_name,"ED01"); // system name
//	strcpy(system_name,"T001"); // system name
	strcpy(serial_number,"106"); // product serial number
	strcpy(component_wabco_number,"0000000112"); // component WABCO number
	strcpy(component_serial_number,"50004"); // component serial number
	
// variables for table with units
	UnitDataPtr *unit_data_tbl; // pointer to table with pointers to UnitData
	int unit_data_cnt; // numer of units
	char unit_name[PRODANGDLL_UNITNAME_SIZE];
	char unit_description[PRODANGDLL_DESCRIPTION_SIZE];
	int i_unit; // variable for "for" loop for table with units

// variables for process definition
	Identification ident; // structure with results from IdentifyMe function.
	Process process; // process
	ProductionLine production_line; // production line
	ProcessStep process_step; // process step
	System system; // system (production station)
	
	// process step parameters (parameters for one station)
	ProcessStepParam process_step_param; // ProcessStepParam structure
	ProcessStepParamPtr *process_step_param_tbl; // pointer to table with pointers to ProcessStepParam structure
	int process_step_param_cnt; // number of process step parameters

	// test steps (test steps executed on one station)
	TestStep	test_step; // TestStep structure
	TestStepPtr	*test_step_tbl; // pointer to table with pointers to TestStep structure
	int test_step_cnt; // number of test steps
	int test_step_tbl_orderby = GETTESTSTEPS_ORDERBY_TEST_SEQUENCE; // how to sort test steps. Possible values are GETTESTSTEPS_ORDERBY_TEST_SEQUENCE and GETTESTSTEPS_ORDERBY_TEST_ORDER. test sequence is always defined in Proda while test order can be undefined (=0 for all steps). Should be in configuration file 

	// test step parameters (variable for all test steps)
	TestStepParam test_step_param; // TestStepParam structure
	TestStepParamPtr *test_step_param_tbl; //pointer to table with pointers to TestStepParam structure
	int test_step_param_cnt; // number of test step parameters
	TestStepParamPtr **test_step_param_tbl_tbl; //table with pointers to table with pointers to TestStepParam structure
	int *test_step_param_cnt_tbl; // table with number of parameters in each test step

	// test values (variables for all test values in all test steps)
	TestValue test_value; // TestValue structure 
	TestValuePtr *test_value_tbl; // pointer to table with pointers to TestValue structure 
	int test_value_cnt; // number of test values
	TestValuePtr **test_value_tbl_tbl; // table with pointers to table with pointers to TestValue structure 
	int *test_value_cnt_tbl; // table with number of test values in each test step


// variables for results
	char start_time[PRODANGDLL_STARTTIME_SIZE]; // start time string, format is independend from PC regional settings. It is: DD.MM.YYYY HH24:MI:SS (Oracle format)
	char end_time[PRODANGDLL_ENDTIME_SIZE]; // end time string, format is independend from PC regional settings. It is: DD.MM.YYYY HH24:MI:SS (Oracle format)
	//product
	Product_lsn	product; // structure for product (_lsn = product with long serial number)
	// process result
	ProcessResult process_result;
	// process step result
	ProcessStepResult process_step_result;
	// previous process step result
	ProcessStepResult previous_process_step_result;
	int previous_process_step_result_status;
	idbID previous_process_step_result_mode=1; // strictly mode = 1 (strict)
	// test step result
	TestStepResult test_step_result;
	// test value result
	TestValueResult test_value_result;
	//component
	Product_lsn	component; // structure for component (_lsn = product with losng serial number)
	WabcoPart component_wabco_part;

// other variables
	int i,j; // variable for "for" loop
	double test_value_min,test_value_max; // test_value.minimum/maximum (limits for test value)
	double test_result; // variable for "measures" (test_value_result.result)
	int	device_status=1; // let's generate status=ok
	int device_repeat=0; // let's generate  "no repeat" status
	int qty_components_in_product = 4;

// initialize the library
	r = InitProDll(1);
	printf("InitProDll: ");
	switch (r){
		case 0:
			printf("ok\n\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// login to the database
	r = Login(db_user,db_pass,db_name, &h1);
	printf("Login: ");
	switch (r){
		case 0:
			printf("ok\n\n");
			break;
		case -1017:
			printf("Oracle error: ORA-1017 invalid username/password; logon denied (suggestion: check db_user or db_pass)\n\n");
			return 0;
		case -12154:
			printf("Oracle error: ORA-12154 TNS: could not resolve the connect identifier specified (suggestion: check db_name, file: tnsnames.ora, file: sqlnet.ora, check ping to Oracle server)\n\n");
			return 0;
		case -12170:
			printf("Oracle error: ORA-12170 TNS:Connect timeout occurred \n\n");
			return 0;
		case -12541:
			printf("Oracle error: ORA-12541 TNS:no listener (host exists but is there Oracle DB? Is listener working on port defined in tnsnames.ora? suggestion: check db_name, file: tnsnames.ora)\n\n");
			return 0;
		default:
			if (r < 0) {
				printf("Oracle error: ORA%d\n\n",r);
			} else {
				printf("error: %d\n\n",r); // error
			}
			return 0;
	}

// set language for strings returned from Proda
	r = SetLanguage(h1,language_id);
	printf("SetLanguage: ");
	switch (r){
		case 0:
			printf("ok\n\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// read all units from database
	r = GetUnits(h1,&unit_data_tbl,&unit_data_cnt);
	printf("GetUnits: ");
	switch (r){
		case 0:
			printf("ok (read %d units)\n\n",unit_data_cnt);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// identify (find) process, process step etc data based on WABCO number and system name. Function return values into structure Identification ident;
	r=IdentifyMe(h1,system_name,wabco_number,0,0,&ident);
	printf("IdentifyMe for wabco_number=\"%s\" and system_name=\"%s\": ",wabco_number,system_name);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" ident.processId: %d\n ident.processStepId: %d\n ident.systemId: %d\n ident.wabcoPartId: %d\n\n",
				     ident.processId,      ident.processStepId,      ident.systemId,      ident.wabcoPartId);
			break;
		case ERROR_NO_DATA:
			printf("error: ERROR_NO_DATA\n\n");
			return 0;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// read process definition
	r=GetProcess(h1,ident.processId,&process);
	printf("GetProcess for processId=\"%d\": ",ident.processId);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" process.id: %d\n process.productionLineId: %d\n process.releaseId: %d\n process.description: %s\n process.mdReason: %s\n process.mdTime: %s\n process.mdUser: %s\n\n",
			         process.id,      process.productionLineId,      process.releaseId,      process.description,      process.mdReason,      process.mdTime,      process.mdUser);
			break;
		case 1403:
			printf("error: Record not found\n\n");
			return 0;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// read production line description, remark: process is executed on production line
	r=GetProductionLine(h1,process.productionLineId,&production_line);
	printf("GetProductionLine for productionLineId=\"%d\": ",process.productionLineId);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" production_line.id: %d\n production_line.description: %s\n\n",
				     production_line.id,      production_line.description);
			break;
		case 1403:
			printf("error: Record not found\n\n");
			return 0;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// read process step definition
	r=GetProcessStep(h1,ident.processStepId,&process_step);
	printf("GetProcessStep for processStepId=\"%d\": ",ident.processStepId);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" process_step.id: %d\n process_step.processId: %d\n process_step.releaseId: %d\n process_step.systemId: %d\n process_step.processSequence: %d\n process_step.description: %s\n process_step.filename: %s\n process_step.limitRed: %.2f\n process_step.limitYellow: %.2f\n process_step.mdReason: %s\n process_step.mdTime: %s\n process_step.mdUser %s\n\n",
				     process_step.id,      process_step.processId,      process_step.releaseId,      process_step.systemId,      process_step.processSequence,      process_step.description,      process_step.filename,      process_step.limitRed,        process_step.limitYellow,        process_step.mdReason,      process_step.mdTime,      process_step.mdUser);
			break;
		case 1403:
			printf("error: Record not found\n\n");
			return 0;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}



// read system (production station) name, should be the same like we already define as system_name; remark: process contains multiple process steps, each process step is executed on system
	r=GetSystem(h1,process_step.systemId,&system);
	printf("GetSystem for systemId=\"%d\": ",process_step.systemId);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" system.id: %d\n system.name: %s\n\n",
				     system.id,      system.name);
			break;
		case 1403:
			printf("error: Record not found\n\n");
			return 0;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// read process step parameters
	r=GetProcessStepParams(h1,ident.processStepId,&process_step_param_tbl,&process_step_param_cnt);
	printf("GetProcessStepParams for processStepId=\"%d\": ",ident.processStepId);
	switch (r){
		case 0:
			printf("ok (read %d process step parameters)\n",process_step_param_cnt);
			for (i=0;i<process_step_param_cnt;i++){
				process_step_param = *process_step_param_tbl[i];
				strcpy(unit_name,"");
				strcpy(unit_description,"");
				// find unit name and description
				for (i_unit=0;i_unit<unit_data_cnt;i_unit++){
					if (unit_data_tbl[i_unit]->id == process_step_param_tbl[i]->unitId) {
						strcpy(unit_name,unit_data_tbl[i_unit]->unitName);
						strcpy(unit_description,unit_data_tbl[i_unit]->description);
						break;
					}
				}
				printf(" parameter: %d\n",i+1);
				printf("  process_step_param.id: %d\n  process_step_param.description: %s\n  process_step_param.paramSequence: %d\n  process_step_param.processStepId: %d\n  process_step_param.unitId: %d\n  process_step_param.value: %.2f\n  process_step_param.mdReason: %s\n  process_step_param.mdTime: %s\n  process_step_param.mdUser %s\n",
					      process_step_param.id,       process_step_param.description,       process_step_param.paramSequence,       process_step_param.processStepId,       process_step_param.unitId,       process_step_param.value,         process_step_param.mdReason,       process_step_param.mdTime,       process_step_param.mdUser);
				printf("  unit_name: %s\n  unit_description: %s\n",
					      unit_name,       unit_description);
			}
			printf("\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}


// read test steps
/*
GETTESTSTEPS_ORDERBY_TEST_SEQUENCE = 0
GETTESTSTEPS_ORDERBY_TEST_ORDER = 1
*/
	r = GetTestSteps_orderby(h1,ident.processStepId,&test_step_tbl,&test_step_cnt,test_step_tbl_orderby);
	printf("GetTestSteps_orderby for processStepId=\"%d\", orderby=\"%d\": ",ident.processStepId,test_step_tbl_orderby);
	switch (r){
		case 0:
			printf("ok (read %d test steps)\n",test_step_cnt);
			for (i=0;i<test_step_cnt;i++){
				test_step = *test_step_tbl[i];
				printf(" step: %d\n",i+1);
				printf("  test_step.id: %d\n  test_step.description: %s\n  test_step.testSequence: %d\n  test_step.testOrder: %d\n  test_step.processStepId: %d\n  test_step.mdReason: %s\n  test_step.mdTime: %s\n  test_step.mdUser %s\n",
						  test_step.id,       test_step.description,       test_step.testSequence,       test_step.testOrder,       test_step.processStepId,       test_step.mdReason,       test_step.mdTime,       test_step.mdUser);
			}
			printf("\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}  

// read test step parameters (for all test steps)
	test_step_param_cnt_tbl=new int[test_step_cnt]; // initialize table to store number of parameters for each test step
	test_step_param_tbl_tbl=new TestStepParamPtr*[test_step_cnt]; // initialize table to store pointers to tables with pointers to test step parameters
	for (i=0;i<test_step_cnt;i++){
		r = GetTestStepParams(h1,test_step_tbl[i]->id,&(test_step_param_tbl_tbl[i]),&(test_step_param_cnt_tbl[i]));
		printf("GetTestStepParams for testStepId=\"%d\": ",test_step_tbl[i]->id);
		switch (r){
			case 0:
				test_step_param_tbl = test_step_param_tbl_tbl[i];
				test_step_param_cnt = test_step_param_cnt_tbl[i];
				printf("ok (read %d test step parameters)\n",test_step_param_cnt);
				for (j=0;j<test_step_param_cnt;j++){
					test_step_param = *test_step_param_tbl[j];
					strcpy(unit_name,"");
					strcpy(unit_description,"");
					// find unit name and description
					for (i_unit=0;i_unit<unit_data_cnt;i_unit++){
						if (unit_data_tbl[i_unit]->id == test_step_param_tbl[j]->unitId) {
							strcpy(unit_name,unit_data_tbl[i_unit]->unitName);
							strcpy(unit_description,unit_data_tbl[i_unit]->description);
							break;
						}
					}
					printf(" parameter: %d\n",j+1);
					printf("  test_step_param.id: %d\n  test_step_param.description: %s\n  test_step_param.paramSequence: %d\n  test_step_param.testStepId: %d\n  test_step_param.unitId: %d\n  test_step_param.value: %.2f\n  test_step_param.mdReason: %s\n  test_step_param.mdTime: %s\n  test_step_param.mdUser %s\n",
						      test_step_param.id,       test_step_param.description,       test_step_param.paramSequence,       test_step_param.testStepId,       test_step_param.unitId,       test_step_param.value,         test_step_param.mdReason,       test_step_param.mdTime,       test_step_param.mdUser);
					printf("  unit_name: %s\n  unit_description: %s\n",
						      unit_name,       unit_description);
				}
				printf("\n");
				break;
			default:
				printf("error: %d\n\n",r); // error
				return 0;
		}  
	}

// read test values (for all test steps)
	test_value_cnt_tbl=new int[test_step_cnt]; // initialize table to store number of parameters for each test step
	test_value_tbl_tbl=new TestValuePtr*[test_step_cnt]; // initialize table to store pointers to tables with pointers to test values
	for (i=0;i<test_step_cnt;i++){
		r = GetTestValues(h1,test_step_tbl[i]->id,&(test_value_tbl_tbl[i]),&(test_value_cnt_tbl[i]));
		printf("GetTestValues for testStepId=\"%d\"; test step sequence/order (description): %d/%d (%s): ",test_step_tbl[i]->id,test_step_tbl[i]->testSequence,test_step_tbl[i]->testOrder,test_step_tbl[i]->description);
		switch (r){
			case 0:
			test_value_tbl = test_value_tbl_tbl[i];
			test_value_cnt = test_value_cnt_tbl[i];
				printf("ok (read %d test values)\n",test_value_cnt);
				for (j=0;j<test_value_cnt;j++){
					test_value = *test_value_tbl[j];
					strcpy(unit_name,"");
					strcpy(unit_description,"");
					// find unit name and description
					for (i_unit=0;i_unit<unit_data_cnt;i_unit++){
						if (unit_data_tbl[i_unit]->id == test_value_tbl[j]->unitId) {
							strcpy(unit_name,unit_data_tbl[i_unit]->unitName);
							strcpy(unit_description,unit_data_tbl[i_unit]->description);
							break;
						}
					}
					printf(" test value: %d\n",j+1);
					printf("  test_value.id: %d\n  test_value.description: %s\n  test_value.testValueSequence: %d\n  test_value.testStepId: %d\n  test_value.unitId: %d\n  test_value.minimum: %.2f\n  test_value.maximum: %.2f\n  test_value.valueText: %s\n  test_value.mdReason: %s\n  test_value.mdTime: %s\n  test_value.mdUser %s\n",
						      test_value.id,       test_value.description,       test_value.testValueSequence,       test_value.testStepId,       test_value.unitId,       test_value.minimum,         test_value.maximum,         test_value.valueText,       test_value.mdReason,       test_value.mdTime,       test_value.mdUser);
					printf("  unit_name: %s\n  unit_description: %s\n",
						      unit_name,       unit_description);
				}
				printf("\n");
				break;
			default:
				printf("error: %d\n\n",r); // error
				return 0;
		}
	}

// write results
	printf("\n-------------------------------------\n    Results writing\n-------------------------------------\n\n",r);
	r = GetDatabaseTime(h1, start_time);
	printf("GetDatabaseTime (start time): ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" %s\n\n",start_time);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	for (i=0;i<1000000;i++) for (j=0;j<1000;j++); // loops to do nothing (waste some time to see difference between start_time and end_time)
	r = GetDatabaseTime(h1, end_time);
	printf("GetDatabaseTime (end time): ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" %s\n\n",end_time);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

/*
------------------------------------------------------------------------------------------------------------------------

Please notice that struct member "id" for results are strings (char[PRODANGDLL_CDBID_SIZE]) not numbers.
Reason is that the int number is limited to 32bits while string (char[PRODANGDLL_CDBID_SIZE]) is PRODANGDLL_CDBID_SIZE=16 digits size.
To set id please use for example: strcpy.
"id" in the database is NUMBER type.

------------------------------------------------------------------------------------------------------------------------
*/



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
	printf("NewProduct_lsn: ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" New product added\n"); // new product is created
			break;
		case ERROR_MORE_DATA:
			printf("ok\n");
			printf(" Product already exists\n"); // this product already exists and NewProduct_lsn function return existing product
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	printf("  product.id: %s\n  product.wabcoPartId: %d\n  product.serialNumber: %s\n  product.individual: %d\n  product.comment: %s\n  product.crProcessStepId: %d\n  product.mdProcessStepId: %d\n  product.crTime: %s\n  product.mdTime: %s\n\n",
		      product.id,       product.wabcoPartId,       product.serialNumber,       product.individual,       product.comment,       product.crProcessStepId,       product.mdProcessStepId,       product.crTime,       product.mdTime);


	/* 
	Process result generating
		Required: productId, processId, statusId
		Optional: startTime (default=sysdate), endTime (default=null)
	*/
	memset(&process_result, 0 , sizeof(process_result)); // clear process_result structure
	strcpy(process_result.productId,product.id); // set productId for product
	process_result.processId=ident.processId; // set processId for process definition
	process_result.statusId=-1; // -1 -> dll decides about status

	r = NewProcessResult(h1,&process_result);
	printf("NewProcessResult: ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" New process result added\n");
			break;
		case ERROR_MORE_DATA:
			printf("ok\n");
			printf(" Process result already exists\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	printf("  process_result.id: %s\n  process_result.processId: %d\n  process_result.productId: %s\n  process_result.statusId: %d\n  process_result.startTime: %s\n  process_result.endTime: %s\n\n",
		      process_result.id,       process_result.processId,       process_result.productId,       process_result.statusId,       process_result.startTime,       process_result.endTime);

// read previus process step status (use in case of storing results for process step which is not a first process step)
/*
strictlyMode defines the behaviour of the function.
0	not strict. The function may return a previous process step result also if the direct previous process step is missing or the chronological order is not correct.
1	strict. The function checks if the previous step with results is the direct predessecor of the supplied one. It also checks the chronological order of all process step results below the previous found. It will return the outcome as different stati in *statusPtr;


statusPtr is a pointer on an Integer, which returns the status of the function outcome if the returncode is 0
-4	Found a result but there exists steps below with newer end time (reported only in strict mode)
-3	Found a result but is not the direct previous step (reported only in strict mode)
-2	No according results found (processStepResult not filled)
-1	No data found (missing process step …) (processStepResult not filled)
*/
	memset(&previous_process_step_result, 0 , sizeof(previous_process_step_result)); // clear previous_process_step_result structure
	r=GetPreviousProcessStepStatus(h1,process_result.id,process_step.id,previous_process_step_result_mode,&previous_process_step_result,&previous_process_step_result_status);
	printf("GetPreviousProcessStepStatus for processStepId=\"%d\" and strictlyMode=\"%d\": ",process_step.id,previous_process_step_result_mode);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" previous_process_step_result_status: %d\n",
				     previous_process_step_result_status);
			printf(" previous_process_step_result.id: %s\n previous_process_step_result.processStepId: %d\n previous_process_step_result.processResultId: %s\n previous_process_step_result.statusId: %d\n previous_process_step_result.startTime: %s\n previous_process_step_result.endTime: %s\n\n",
				     previous_process_step_result.id,      previous_process_step_result.processStepId,      previous_process_step_result.processResultId,      previous_process_step_result.statusId,      previous_process_step_result.startTime,      previous_process_step_result.endTime);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

	/* 
	Process step result generating
		Required: processStepId, processResultId, statusId
		Optional: startTime (default=sysdate), endTime (default=null), operatorId (default=null)
	*/
	memset(&process_step_result, 0 , sizeof(process_step_result)); // clear process_step_result structure
	process_step_result.processStepId=process_step.id; // set processStepId for process_step definition
	strcpy(process_step_result.processResultId,process_result.id); // set processResultId for process result
	process_step_result.statusId=-1; // -1 -> dll decide about status
	process_step_result.operatorId=43375; // set operator id, this is int number. This field gives us possibility to tell to the system who was working on the station to build product

	r = NewProcessStepResult(h1,&process_step_result);
	printf("NewProcessStepResult: ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" process_step_result.id: %s\n process_step_result.processStepId: %d\n process_step_result.processResultId: %s\n process_step_result.statusId: %d\n process_step_result.startTime: %s\n process_step_result.endTime: %s\n\n",
				     process_step_result.id,      process_step_result.processStepId,      process_step_result.processResultId,      process_step_result.statusId,      process_step_result.startTime,      process_step_result.endTime);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// test step results generating
	for (i=0;i<test_step_cnt;i++){ // save all test steps
		/* 
		Test step result generating
			Required: processStepResultId, testStepId, statusId
		*/
		memset(&test_step_result, 0 , sizeof(test_step_result)); // clear process_step_result structure
		test_step_result.testStepId=test_step_tbl[i]->id; // set testStepId for test step definition
		strcpy(test_step_result.processStepResultId,process_step_result.id); // set processStepResultId for process step result
		test_step_result.statusId=-1; // -1 -> dll decide about status
		r = NewTestStepResult(h1,&test_step_result); // begin test step result creation
		printf("NewTestStepResult for testStepId=\"%d\"; test step sequence/order (description): %d/%d (%s): ",test_step_tbl[i]->id,test_step_tbl[i]->testSequence,test_step_tbl[i]->testOrder,test_step_tbl[i]->description);
		switch (r){
			case 0:
				printf("ok\n");
				printf(" test_step_result.id: %s\n test_step_result.processStepResultId: %s\n test_step_result.testStepId: %d\n test_step_result.statusId: %d\n\n",
					     test_step_result.id,      test_step_result.processStepResultId,      test_step_result.testStepId,      test_step_result.statusId);
				break;
			default:
				printf("error: %d\n\n",r); // error
				return 0;
		}

	// test values for test step
		test_value_tbl = test_value_tbl_tbl[i];
		test_value_cnt = test_value_cnt_tbl[i];
		for (j=0;j<test_value_cnt;j++){
			test_value_min=test_value_tbl[j]->minimum;
			test_value_max=test_value_tbl[j]->maximum;
			if (device_status==1) { // let supppose that device pass the test
				test_result=(double)rand()/(double)RAND_MAX; //0...1
				test_result*=(test_value_max-test_value_min);
				test_result+=test_value_min;
			} else { // let supppose that device didn't pass the test
				test_result=(double)rand()/(double)RAND_MAX; //0...1
				test_result*=(test_value_max-test_value_min)*5;
				test_result+=test_value_min-(test_value_max-test_value_min)*2;
			}
			/* 
			Test value generating
				Required: testStepResultId, testValueId, result, statusId
				Optional: contentId (defalt=null)
			*/
			memset(&test_value_result, 0 , sizeof(test_value_result)); // clear test_value_result structure
			test_value_result.result=test_result;
			test_value_result.statusId=-1; // -1 -> dll decide about status
			test_value_result.testValueId=test_value_tbl[j]->id;
			strcpy(test_value_result.testStepResultId,test_step_result.id);
			r = NewTestValueResult(h1,&test_value_result); // begin test value result creation
			printf("NewTestValueResult for testValueId=\"%d\"; test value sequence (description): %d (%s): ",test_value_tbl[j]->id,test_value_tbl[j]->testValueSequence,test_value_tbl[j]->description);
			switch (r){
				case 0:
					printf("ok\n");
					printf(" test_value_result.id: %s\n test_value_result.testStepResultId: %s\n test_value_result.testValueId: %d\n test_value_result.result: %.3f\n test_value_result.statusId: %d\n\n",
							 test_value_result.id,      test_value_result.testStepResultId,      test_value_result.testValueId,      test_value_result.result,        test_value_result.statusId);
					break;
				default:
					printf("error: %d\n\n",r); // error
					return 0;
			}
			/*
			finish test value creation
				Required: id, testStepResultId, testValueId, result, statusId
				Optional: contentId (defalt=null)
				Advise: provide structure returned by NewValueResult; if statusId in NewTestValueResult was already set to correct value (by set -1 or required value) then avoid set it again to -1 to avoid performance drop.
			*/
			r = SetTestValueResult(h1,0,&test_value_result); // finish test value result creation, isRepeat=0 as we do not repeat measurements
			printf("SetTestValueResult for testValueId=\"%d\"; test value sequence (description): %d (%s): ",test_value_tbl[j]->id,test_value_tbl[j]->testValueSequence,test_value_tbl[j]->description);
			switch (r){
				case 0:
					printf("ok\n");
					printf(" test_value_result.id: %s\n test_value_result.testStepResultId: %s\n test_value_result.testValueId: %d\n test_value_result.result: %.3f\n test_value_result.statusId: %d\n\n",
							 test_value_result.id,      test_value_result.testStepResultId,      test_value_result.testValueId,      test_value_result.result,        test_value_result.statusId);
					break;
				default:
					printf("error: %d\n\n",r); // error
					return 0;
			}
		}
		/*
		finish test step result creation
			Required: id, processStepResultId, testStepId, statusId
			Advise: provide structure returned by NewTestStepResult and update statusId (-1/-3 to do automatic status calculation or required status).
		*/
		test_step_result.statusId=-1;
		r = SetTestStepResult(h1,0,&test_step_result); // finish test step result creation, isRepeat=0 as we do not repeat steps
		printf("SetTestStepResult for testStepId=\"%d\"; test step sequence/order (description): %d/%d (%s): ",test_step_tbl[i]->id,test_step_tbl[i]->testSequence,test_step_tbl[i]->testOrder,test_step_tbl[i]->description);
		switch (r){
			case 0:
				printf("ok\n");
				printf(" test_step_result.id: %s\n test_step_result.processStepResultId: %s\n test_step_result.testStepId: %d\n test_step_result.statusId: %d\n\n",
					     test_step_result.id,      test_step_result.processStepResultId,      test_step_result.testStepId,      test_step_result.statusId);
				break;
			default:
				printf("error: %d\n\n",r); // error
				return 0;
		}
	}
													  
	/*
	finish process step result creation
		Required: id, processStepId, processResultId, statusId, startTime
		Optional: endTime (default=sysdate), operatorId (default=null)
		Advise: provide structure returned by NewProcessStepResult and update statusId (-1/-3 to do automatic status calculation or set required status), start__time, end_time
	*/
	strcpy(process_step_result.startTime,start_time); // set start time for process step (station)
	strcpy(process_step_result.endTime,end_time); // set end time for process step (station)
	process_step_result.statusId=-1; // -1 -> dll decide about status
	r = SetProcessStepResult(h1,device_repeat,&process_step_result); // finish process step result creation
	printf("SetProcessStepResult: ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" process_step_result.id: %s\n process_step_result.processStepId: %d\n process_step_result.processResultId: %s\n process_step_result.statusId: %d\n process_step_result.startTime: %s\n process_step_result.endTime: %s\n\n",
				     process_step_result.id,      process_step_result.processStepId,      process_step_result.processResultId,      process_step_result.statusId,      process_step_result.startTime,      process_step_result.endTime);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	/*
	finish process result creation
		Required: id, productId, processId, statusId, startTime
		Optional: endTime (default=sysdate)
		Advise: provide structure returned by NewProcessResult and update statusId (-1/-3 to do automatic status calculation or 1/2 to set required status).
	*/
	process_result.statusId=-1; // -1 -> dll decide about status
	r = SetProcessResult(h1,&process_result); // finish process result creation
	printf("SetProcessResult: ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" process_result.id: %s\n process_result.processId: %d\n process_result.productId: %s\n process_result.statusId: %d\n process_result.startTime: %s\n process_result.endTime: %s\n\n",
				     process_result.id,      process_result.processId,      process_result.productId,      process_result.statusId,      process_result.startTime,      process_result.endTime);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

	/*
	finish product creation
		Required: id, wabcoPartId, serialNumber, individual,
		Optional: comment, mdTime (default=sysdate), mdProcessStepId (0=null)
		Advise: provide structure filled by NewProduct without any changes
	*/
	r = SetProduct_lsn(h1,&product); // finish product creation, 
	printf("SetProduct_lsn: ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" product.id: %s\n product.wabcoPartId: %d\n product.serialNumber: %s\n product.individual: %d\n product.comment: %s\n product.crProcessStepId: %d\n product.mdProcessStepId: %d\n product.crTime: %s\n product.mdTime: %s\n\n",
					 product.id,      product.wabcoPartId,      product.serialNumber,      product.individual,      product.comment,      product.crProcessStepId,      product.mdProcessStepId,      product.crTime,      product.mdTime);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

// add component to product
	strcpy(component_wabco_part.wabcoNumber,component_wabco_number); // clear component_wabco_number structure
	r = GetWabcoPart(h1,-1,&component_wabco_part); // -1 => return component_wabco_part for defined wabco_number in the structure
	printf("GetWabcoPart (component) for WABCO number=\"%s\": ",component_wabco_number);
	switch (r){
		case 0:
			printf("ok\n");
			printf(" component_wabco_part.id: %d\n component_wabco_part.workCenterId: %d\n component_wabco_part.productName: %s\n component_wabco_part.wabcoNumber: %s\n component_wabco_part.mdReason: %s\n component_wabco_part.mdTime: %s\n component_wabco_part.mdUser: %s\n\n",
					 component_wabco_part.id,      component_wabco_part.workCenterId,      component_wabco_part.productName,      component_wabco_part.wabcoNumber,      component_wabco_part.mdReason,      component_wabco_part.mdTime,      component_wabco_part.mdUser);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

	/*
	Product (for component) generating
	initialize product structure members
		Required: wabcoPartId, serialNumber, individual
		Optional: comment (default=null), crProcessStepId (default=null), crTime (default=sysdate), mdTime (default=crTime)
	*/
	memset(&component, 0, sizeof(component)); // clear component structure
	component.wabcoPartId=component_wabco_part.id; // set wabco part id
	strcpy(component.serialNumber,component_serial_number); // serial number for product
	component.individual=1; // set whether product is with SN (individual=1) or without SN (individual=0)
	strcpy(component.comment,"added from test program, v. 1.234"); // comment for product, ex. version of test program

	r = NewProduct_lsn(h1,&component); // create component (this is a product in the database)
	printf("NewProduct_lsn (component): ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" New product added\n"); // new product is created
			break;
		case ERROR_MORE_DATA:
			printf("ok\n");
			printf(" Product already exists\n"); // this product already exists and NewProduct_lsn function return existing product
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	printf("  component.id: %s\n  component.wabcoPartId: %d\n  component.serialNumber: %s\n  component.individual: %d\n  component.comment: %s\n  component.crProcessStepId: %d\n  component.mdProcessStepId: %d\n  component.crTime: %s\n  component.mdTime: %s\n\n",
		      component.id,       component.wabcoPartId,       component.serialNumber,       component.individual,       component.comment,       component.crProcessStepId,       component.mdProcessStepId,       component.crTime,       component.mdTime);

	/*
	finish component creation
		Required: id, wabcoPartId, serialNumber, individual,
		Optional: comment, mdTime (default=sysdate), mdProcessStepId (0=null)
		Advise: provide structure filled by NewProduct without any changes
	*/
	r=SetProduct_lsn(h1,&component);  // finish component creation
	printf("SetProduct_lsn (component): ");
	switch (r){
		case 0:
			printf("ok\n");
			printf(" component.id: %s\n component.wabcoPartId: %d\n component.serialNumber: %s\n component.individual: %d\n component.comment: %s\n component.crProcessStepId: %d\n component.mdProcessStepId: %d\n component.crTime: %s\n component.mdTime: %s\n\n",
				     component.id,      component.wabcoPartId,      component.serialNumber,      component.individual,      component.comment,      component.crProcessStepId,      component.mdProcessStepId,      component.crTime,      component.mdTime);
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}

	// add component to product
	r = AddComponent_wabcoNumber_serialNumber(h1,wabco_number,serial_number,component_wabco_number,component_serial_number,"",qty_components_in_product);
	printf("AddComponent_wabcoNumber_serialNumber for product wabco_number=\"%s\" and product serial_number=\"%s\" and component wabco_number=\"%s\" and component serial_number=\"%s\" and qty=\"%d\": ",wabco_number,serial_number,component_wabco_number,component_serial_number,qty_components_in_product);
	switch (r){
		case 0:
			printf("ok\n\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	r = Logout(h1); // logout from database
	printf("Logout: ");
	switch (r){
		case 0:
			printf("ok\n\n");
			break;
		default:
			printf("error: %d\n\n",r); // error
			return 0;
	}
	ExitProDll();
	
	FreeStructArray((void **)unit_data_tbl);
	FreeStructArray((void **)process_step_param_tbl);
	FreeStructArray((void **)test_step_tbl);
	for (i=0;i<test_step_cnt;i++){
		test_value_tbl = test_value_tbl_tbl[i];
		test_step_param_tbl = test_step_param_tbl_tbl[i];
		FreeStructArray((void **)test_value_tbl);
		FreeStructArray((void **)test_step_param_tbl);
	}
	return 0;
}
