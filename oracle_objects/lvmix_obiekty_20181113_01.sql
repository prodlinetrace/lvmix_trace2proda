--DROP TABLE PRODANG_CONVERT.TEST_LVMIX CASCADE CONSTRAINTS;

CREATE TABLE PRODANG_CONVERT.TEST_LVMIX
(
  WABCO_NUMBER             VARCHAR2(10 BYTE),
  PROCESS_STEP_SEQUENCE    NUMBER,
  SERIAL_NUMBER            VARCHAR2(1000 BYTE),
  XCOMMENT                 VARCHAR2(256 BYTE),
  PROCESS_START_TIME       DATE,
  PROCESS_END_TIME         DATE,
  PROCESS_STATUS           NUMBER,
  PROCESS_STEP_START_TIME  DATE,
  PROCESS_STEP_END_TIME    DATE,
  PROCESS_STEP_STATUS      NUMBER,
  OPERATOR_ID              NUMBER,
  RESULT_001               VARCHAR2(100 BYTE),
  RESULT_002               VARCHAR2(100 BYTE),
  RESULT_003               VARCHAR2(100 BYTE),
  RESULT_004               VARCHAR2(100 BYTE),
  RESULT_005               VARCHAR2(100 BYTE),
  RESULT_006               VARCHAR2(100 BYTE),
  RESULT_007               VARCHAR2(100 BYTE),
  RESULT_008               VARCHAR2(100 BYTE),
  RESULT_009               VARCHAR2(100 BYTE),
  RESULT_010               VARCHAR2(100 BYTE),
  RESULT_011               VARCHAR2(100 BYTE),
  RESULT_012               VARCHAR2(100 BYTE),
  RESULT_013               VARCHAR2(100 BYTE),
  RESULT_014               VARCHAR2(100 BYTE),
  RESULT_015               VARCHAR2(100 BYTE),
  RESULT_016               VARCHAR2(100 BYTE),
  RESULT_017               VARCHAR2(100 BYTE),
  RESULT_018               VARCHAR2(100 BYTE),
  RESULT_019               VARCHAR2(100 BYTE),
  RESULT_020               VARCHAR2(100 BYTE),
  RESULT_021               VARCHAR2(100 BYTE),
  RESULT_022               VARCHAR2(100 BYTE),
  RESULT_023               VARCHAR2(100 BYTE),
  RESULT_024               VARCHAR2(100 BYTE),
  RESULT_025               VARCHAR2(100 BYTE),
  RESULT_026               VARCHAR2(100 BYTE),
  RESULT_027               VARCHAR2(100 BYTE),
  RESULT_028               VARCHAR2(100 BYTE),
  RESULT_029               VARCHAR2(100 BYTE),
  RESULT_030               VARCHAR2(100 BYTE),
  RESULT_031               VARCHAR2(100 BYTE),
  RESULT_032               VARCHAR2(100 BYTE),
  RESULT_033               VARCHAR2(100 BYTE),
  RESULT_034               VARCHAR2(100 BYTE),
  RESULT_035               VARCHAR2(100 BYTE),
  RESULT_036               VARCHAR2(100 BYTE),
  RESULT_037               VARCHAR2(100 BYTE),
  RESULT_038               VARCHAR2(100 BYTE),
  RESULT_039               VARCHAR2(100 BYTE),
  RESULT_040               VARCHAR2(100 BYTE),
  RESULT_041               VARCHAR2(100 BYTE),
  RESULT_042               VARCHAR2(100 BYTE),
  RESULT_043               VARCHAR2(100 BYTE),
  RESULT_044               VARCHAR2(100 BYTE),
  RESULT_045               VARCHAR2(100 BYTE),
  RESULT_046               VARCHAR2(100 BYTE),
  RESULT_047               VARCHAR2(100 BYTE),
  RESULT_048               VARCHAR2(100 BYTE),
  RESULT_049               VARCHAR2(100 BYTE),
  RESULT_050               VARCHAR2(100 BYTE),
  RESULT_051               VARCHAR2(100 BYTE),
  RESULT_052               VARCHAR2(100 BYTE),
  RESULT_053               VARCHAR2(100 BYTE),
  RESULT_054               VARCHAR2(100 BYTE),
  RESULT_055               VARCHAR2(100 BYTE),
  RESULT_056               VARCHAR2(100 BYTE),
  RESULT_057               VARCHAR2(100 BYTE),
  RESULT_058               VARCHAR2(100 BYTE),
  RESULT_059               VARCHAR2(100 BYTE),
  RESULT_060               VARCHAR2(100 BYTE),
  RESULT_061               VARCHAR2(100 BYTE),
  RESULT_062               VARCHAR2(100 BYTE),
  RESULT_063               VARCHAR2(100 BYTE),
  RESULT_064               VARCHAR2(100 BYTE),
  RESULT_065               VARCHAR2(100 BYTE),
  RESULT_066               VARCHAR2(100 BYTE),
  RESULT_067               VARCHAR2(100 BYTE),
  RESULT_068               VARCHAR2(100 BYTE),
  RESULT_069               VARCHAR2(100 BYTE),
  RESULT_070               VARCHAR2(100 BYTE),
  RESULT_071               VARCHAR2(100 BYTE),
  RESULT_072               VARCHAR2(100 BYTE),
  RESULT_073               VARCHAR2(100 BYTE),
  RESULT_074               VARCHAR2(100 BYTE),
  RESULT_075               VARCHAR2(100 BYTE),
  RESULT_076               VARCHAR2(100 BYTE),
  RESULT_077               VARCHAR2(100 BYTE),
  RESULT_078               VARCHAR2(100 BYTE),
  RESULT_079               VARCHAR2(100 BYTE),
  RESULT_080               VARCHAR2(100 BYTE),
  RESULT_081               VARCHAR2(100 BYTE),
  RESULT_082               VARCHAR2(100 BYTE),
  RESULT_083               VARCHAR2(100 BYTE),
  RESULT_084               VARCHAR2(100 BYTE),
  RESULT_085               VARCHAR2(100 BYTE),
  RESULT_086               VARCHAR2(100 BYTE),
  RESULT_087               VARCHAR2(100 BYTE),
  RESULT_088               VARCHAR2(100 BYTE),
  RESULT_089               VARCHAR2(100 BYTE),
  RESULT_090               VARCHAR2(100 BYTE),
  RESULT_091               VARCHAR2(100 BYTE),
  RESULT_092               VARCHAR2(100 BYTE),
  RESULT_093               VARCHAR2(100 BYTE),
  RESULT_094               VARCHAR2(100 BYTE),
  RESULT_095               VARCHAR2(100 BYTE),
  RESULT_096               VARCHAR2(100 BYTE),
  RESULT_097               VARCHAR2(100 BYTE),
  RESULT_098               VARCHAR2(100 BYTE),
  RESULT_099               VARCHAR2(100 BYTE),
  RESULT_100               VARCHAR2(100 BYTE)
);

--DROP VIEW PRODANG_CONVERT.VW_TEST_LVMIX;

/* Formatted on 2018-11-08 07:37:44 (QP5 v5.336) */
CREATE OR REPLACE FORCE VIEW PRODANG_CONVERT.VW_TEST_LVMIX
(
    WABCO_NUMBER,
    PROCESS_STEP_SEQUENCE,
    SERIAL_NUMBER,
    XCOMMENT,
    PROCESS_START_TIME,
    PROCESS_END_TIME,
    PROCESS_STATUS,
    PROCESS_STEP_START_TIME,
    PROCESS_STEP_END_TIME,
    PROCESS_STEP_STATUS,
    OPERATOR_ID,
    RESULT_001,
    RESULT_002,
    RESULT_003,
    RESULT_004,
    RESULT_005,
    RESULT_006,
    RESULT_007,
    RESULT_008,
    RESULT_009,
    RESULT_010,
    RESULT_011,
    RESULT_012,
    RESULT_013,
    RESULT_014,
    RESULT_015,
    RESULT_016,
    RESULT_017,
    RESULT_018,
    RESULT_019,
    RESULT_020,
    RESULT_021,
    RESULT_022,
    RESULT_023,
    RESULT_024,
    RESULT_025,
    RESULT_026,
    RESULT_027,
    RESULT_028,
    RESULT_029,
    RESULT_030,
    RESULT_031,
    RESULT_032,
    RESULT_033,
    RESULT_034,
    RESULT_035,
    RESULT_036,
    RESULT_037,
    RESULT_038,
    RESULT_039,
    RESULT_040,
    RESULT_041,
    RESULT_042,
    RESULT_043,
    RESULT_044,
    RESULT_045,
    RESULT_046,
    RESULT_047,
    RESULT_048,
    RESULT_049,
    RESULT_050,
    RESULT_051,
    RESULT_052,
    RESULT_053,
    RESULT_054,
    RESULT_055,
    RESULT_056,
    RESULT_057,
    RESULT_058,
    RESULT_059,
    RESULT_060,
    RESULT_061,
    RESULT_062,
    RESULT_063,
    RESULT_064,
    RESULT_065,
    RESULT_066,
    RESULT_067,
    RESULT_068,
    RESULT_069,
    RESULT_070,
    RESULT_071,
    RESULT_072,
    RESULT_073,
    RESULT_074,
    RESULT_075,
    RESULT_076,
    RESULT_077,
    RESULT_078,
    RESULT_079,
    RESULT_080,
    RESULT_081,
    RESULT_082,
    RESULT_083,
    RESULT_084,
    RESULT_085,
    RESULT_086,
    RESULT_087,
    RESULT_088,
    RESULT_089,
    RESULT_090,
    RESULT_091,
    RESULT_092,
    RESULT_093,
    RESULT_094,
    RESULT_095,
    RESULT_096,
    RESULT_097,
    RESULT_098,
    RESULT_099,
    RESULT_100
)
AS
    SELECT "WABCO_NUMBER",
           "PROCESS_STEP_SEQUENCE",
           "SERIAL_NUMBER",
           "XCOMMENT",
           "PROCESS_START_TIME",
           "PROCESS_END_TIME",
           "PROCESS_STATUS",
           "PROCESS_STEP_START_TIME",
           "PROCESS_STEP_END_TIME",
           "PROCESS_STEP_STATUS",
           "OPERATOR_ID",
           "RESULT_001",
           "RESULT_002",
           "RESULT_003",
           "RESULT_004",
           "RESULT_005",
           "RESULT_006",
           "RESULT_007",
           "RESULT_008",
           "RESULT_009",
           "RESULT_010",
           "RESULT_011",
           "RESULT_012",
           "RESULT_013",
           "RESULT_014",
           "RESULT_015",
           "RESULT_016",
           "RESULT_017",
           "RESULT_018",
           "RESULT_019",
           "RESULT_020",
           "RESULT_021",
           "RESULT_022",
           "RESULT_023",
           "RESULT_024",
           "RESULT_025",
           "RESULT_026",
           "RESULT_027",
           "RESULT_028",
           "RESULT_029",
           "RESULT_030",
           "RESULT_031",
           "RESULT_032",
           "RESULT_033",
           "RESULT_034",
           "RESULT_035",
           "RESULT_036",
           "RESULT_037",
           "RESULT_038",
           "RESULT_039",
           "RESULT_040",
           "RESULT_041",
           "RESULT_042",
           "RESULT_043",
           "RESULT_044",
           "RESULT_045",
           "RESULT_046",
           "RESULT_047",
           "RESULT_048",
           "RESULT_049",
           "RESULT_050",
           "RESULT_051",
           "RESULT_052",
           "RESULT_053",
           "RESULT_054",
           "RESULT_055",
           "RESULT_056",
           "RESULT_057",
           "RESULT_058",
           "RESULT_059",
           "RESULT_060",
           "RESULT_061",
           "RESULT_062",
           "RESULT_063",
           "RESULT_064",
           "RESULT_065",
           "RESULT_066",
           "RESULT_067",
           "RESULT_068",
           "RESULT_069",
           "RESULT_070",
           "RESULT_071",
           "RESULT_072",
           "RESULT_073",
           "RESULT_074",
           "RESULT_075",
           "RESULT_076",
           "RESULT_077",
           "RESULT_078",
           "RESULT_079",
           "RESULT_080",
           "RESULT_081",
           "RESULT_082",
           "RESULT_083",
           "RESULT_084",
           "RESULT_085",
           "RESULT_086",
           "RESULT_087",
           "RESULT_088",
           "RESULT_089",
           "RESULT_090",
           "RESULT_091",
           "RESULT_092",
           "RESULT_093",
           "RESULT_094",
           "RESULT_095",
           "RESULT_096",
           "RESULT_097",
           "RESULT_098",
           "RESULT_099",
           "RESULT_100"
      FROM PRODANG_CONVERT.TEST_LVMIX;


CREATE OR REPLACE TRIGGER PRODANG_CONVERT.VW_TEST_LVMIX_TRG
INSTEAD OF INSERT
ON PRODANG_CONVERT.VW_TEST_LVMIX
REFERENCING NEW AS NEW OLD AS OLD
FOR EACH ROW
DECLARE
/*
   wabco_number,
   process_step_sequence,
   serial_number,
   xcomment,
   process_start_time,
   process_end_time,
   process_status,
   process_step_start_time,
   process_step_end_time,
   process_step_status,
   operator_id,
   result_001,
   result_002,
   result_003,

*/
    v_wabco_number              wabcopart.wabco_number%type;
    v_process_step_sequence     process_step.process_sequence%type;
    v_serial_number             product.serial_number%type;
    v_xcomment                  product.xcomment%type;
    v_process_start_time        process_result.start_time%type;
    v_process_end_time          process_result.end_time%type;
    v_process_status            process_result.status_id%type;
    v_process_step_start_time   process_step_result.start_time%type;
    v_process_step_end_time     process_step_result.end_time%type;
    v_process_step_status       process_step_result.status_id%type;
    v_operator_id               process_step_result.operator_id%type;

    v_result                    test_lvmix.result_001%type;
    type results is table of test_lvmix.result_001%type;
    v_results                   results;
    
    v_db_id                     preference_value.value_as_number%type;
    v_wabcopart_id              wabcopart.id%type;
    v_process_id                process.id%type;
    v_process_step_id           process_step.id%type;
    v_test_step_id              test_step.id%type;
    v_test_value_id             test_value.id%type;
    v_test_order             test_step.test_sequence%type;
    v_test_value_sequence       test_value.test_value_sequence%type;
    v_product_id                product.id%type;
    v_process_result_id         process_result.id%type;
    v_process_step_result_id    process_step_result.id%type;
    v_test_step_result_id       test_step_result.id%type;
    v_test_value_result_id      test_value_result.id%type;
  
    type test_value_rec is record
    (
        test_value_id           test_value.id%type,
        test_value_result_id    test_value_result.id%type,
        status                  test_value_result.status_id%type,
        result                  test_value_result.result%type
    );
    type test_value_arr is table of test_value_rec index by pls_integer;

    type test_step_rec is record
    (
        test_step_id            test_step.id%type,
        test_step_result_id     test_step_result.id%type,
        status                  test_value_result.status_id%type,
        test_value_tbl          test_value_arr
    );
    type test_step_arr is table of test_step_rec index by pls_integer;
    
    v_test_step_tbl               test_step_arr;
    v_test_step_status            test_step_result.status_id%type;
    v_test_value_status           test_value_result.status_id%type;
    v_test_value_result           test_value_result.result%type;
    
begin
    v_wabco_number              := :new.wabco_number;
    v_process_step_sequence     := :new.process_step_sequence;
    v_serial_number             := :new.serial_number;
    v_xcomment                  := :new.xcomment;
    v_process_start_time        := :new.process_start_time;
    v_process_end_time          := :new.process_end_time;
    v_process_status            := :new.process_status;
    v_process_step_start_time   := :new.process_step_start_time;
    v_process_step_end_time     := :new.process_step_end_time;
    v_process_step_status       := :new.process_step_status;
    v_operator_id               := :new.operator_id;
    v_results                   := results(:new.result_001,:new.result_002,:new.result_003,:new.result_004,:new.result_005,:new.result_006,:new.result_007,:new.result_008,:new.result_009,:new.result_010,:new.result_011,:new.result_012,:new.result_013,:new.result_014,:new.result_015,:new.result_016,:new.result_017,:new.result_018,:new.result_019,:new.result_020,:new.result_021,:new.result_022,:new.result_023,:new.result_024,:new.result_025,:new.result_026,:new.result_027,:new.result_028,:new.result_029,:new.result_030,:new.result_031,:new.result_032,:new.result_033,:new.result_034,:new.result_035,:new.result_036,:new.result_037,:new.result_038,:new.result_039,:new.result_040,:new.result_041,:new.result_042,:new.result_043,:new.result_044,:new.result_045,:new.result_046,:new.result_047,:new.result_048,:new.result_049,:new.result_050,:new.result_051,:new.result_052,:new.result_053,:new.result_054,:new.result_055,:new.result_056,:new.result_057,:new.result_058,:new.result_059,:new.result_060,:new.result_061,:new.result_062,:new.result_063,:new.result_064,:new.result_065,:new.result_066,:new.result_067,:new.result_068,:new.result_069,:new.result_070,:new.result_071,:new.result_072,:new.result_073,:new.result_074,:new.result_075,:new.result_076,:new.result_077,:new.result_078,:new.result_079,:new.result_080,:new.result_081,:new.result_082,:new.result_083,:new.result_084,:new.result_085,:new.result_086,:new.result_087,:new.result_088,:new.result_089,:new.result_090,:new.result_091,:new.result_092,:new.result_093,:new.result_094,:new.result_095,:new.result_096,:new.result_097,:new.result_098,:new.result_099,:new.result_100);

    if (length(nvl(v_wabco_number,'x')) != 10)
    then
        raise_application_error(-20001,'wabco_number should be 10 characers string.');
    end if;
    begin
        select id into v_wabcopart_id from wabcopart where wabco_number = v_wabco_number;
    exception
        when no_data_found then
        raise_application_error(-20002,'wabco_number '||v_wabco_number||' not found.');
    end;
    
    begin
        select process.id, process_step.id into v_process_id, v_process_step_id
            from wabcopart_process
            join process on wabcopart_process.process_id = process.id
            join process_step on process.id = process_step.process_id
            join systems on process_step.system_id = systems.id
            where wabcopart_process.wabco_part_id = v_wabcopart_id
            and process.release_id = 1
            and process_step.release_id = 1
            and systems.name like 'LV_MIX%'
            and process_step.process_sequence = v_process_step_sequence;
    exception
        when no_data_found then
        raise_application_error(-20003,'There is no released process/process step for wabco_number='||v_wabco_number||' and process_step_sequence='||v_process_step_sequence||'.');
        when too_many_rows then
        raise_application_error(-20004,'There are more than one released process/process step for wabco_number='||v_wabco_number||' and process_step_sequence='||v_process_step_sequence||'.');
    end;
    
    for ts_tv in
    (
        select 
            test_step.id test_step_id, test_value.id test_value_id,
            test_step.test_sequence test_sequence, test_step.test_order test_order, test_value.test_value_sequence test_value_sequence
            from test_step
            join test_value on test_step.id = test_value.test_step_id
            where test_step.process_step_id = v_process_step_id
            and test_step.release_id = 1
            and test_value.release_id = 1
            order by test_step.test_sequence,test_value.test_value_sequence
    )
    loop
        v_test_step_id          := ts_tv.test_step_id;
        v_test_value_id         := ts_tv.test_value_id;
        v_test_order            := ts_tv.test_order;
        v_test_value_sequence   := ts_tv.test_value_sequence;
        v_test_step_tbl(v_test_order).test_step_id           := v_test_step_id;
        v_test_step_tbl(v_test_order).test_step_result_id    := null;
        v_test_step_tbl(v_test_order).status                 := null;
        v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_id        := v_test_value_id;
        v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_result_id := null;
        v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).status               := null;
        v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).result               := null;
    end loop;

    -- process TS_TSSequence_TSStatus
    for v_i in 1..100
    loop
        v_result := v_results(v_i);
        if (v_result is not null)
        then
            v_test_order := to_number(regexp_substr(v_result,'^TS_(\d+)_(0|1)$',1,1,'',1));
            if (v_test_order is not null) --TS_TSOrder_TSStatus
            then
                v_test_step_status := to_number(regexp_substr(v_result,'^TS_(\d+)_(0|1)$',1,1,'',2));
                if (v_test_step_status is null)
                then
                    v_test_order := null;
                end if;
                v_test_value_sequence := null;
            else -- TV_TSSequence_TSOrder_TVStatus_Result
                v_test_order := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',1));
                v_test_value_sequence := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',2));
                v_test_value_status := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',3));
                v_test_value_result := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',4));
                if (v_test_order is null or v_test_value_status is null or v_test_value_result is null)
                then
                    v_test_order := null;
                end if;
            end if;
            if (v_test_order is null)
            then
                raise_application_error(-20005,'result_'||substr('00'||v_i,-3)||' = '||v_result||' is incorrect.');
            end if;
            if (v_test_value_sequence is null)
            then
                begin
                    v_test_step_id := v_test_step_tbl(v_test_order).test_step_id;
                exception
                when no_data_found then
                    raise_application_error(-20006,'result_'||substr('00'||v_i,-3)||' = '||v_result||' is incorrect.');
                end;
                v_test_step_tbl(v_test_order).test_step_result_id    := null;
                v_test_step_tbl(v_test_order).status                 := v_test_step_status;
            end if;
        end if;
    end loop;

    -- process TV_TSSequence_TVSequence_TVStatus_Result
    for v_i in 1..100
    loop
        v_result := v_results(v_i);
        if (v_result is not null)
        then
            v_test_order := to_number(regexp_substr(v_result,'^TS_(\d+)_(0|1)$',1,1,'',1));
            if (v_test_order is not null) --TS_TSSequence_TSStatus
            then
                v_test_step_status := to_number(regexp_substr(v_result,'^TS_(\d+)_(0|1)$',1,1,'',2));
                if (v_test_step_status is null)
                then
                    v_test_order := null;
                end if;
                v_test_value_sequence := null;
            else -- TV_TSSequence_TVSequence_TVStatus_Result
                v_test_order := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',1));
                v_test_value_sequence := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',2));
                v_test_value_status := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',3));
                v_test_value_result := to_number(regexp_substr(v_result,'^TV_(\d+)_(\d+)_(0|1)_(-{0,1}\d+\.{0,1}\d{0,})$',1,1,'',4));
                if (v_test_order is null or v_test_value_status is null or v_test_value_result is null)
                then
                    v_test_order := null;
                end if;
            end if;
            if (v_test_order is null)
            then
                raise_application_error(-20007,'result_'||substr('00'||v_i,-3)||' = '||v_result||' is incorrect.');
            end if;
            if (v_test_value_sequence is not null)
            then
                begin
                    v_test_step_status := v_test_step_tbl(v_test_order).status;
                exception
                when no_data_found then
                    raise_application_error(-20008,'result_'||substr('00'||v_i,-3)||' = '||v_result||' is incorrect.');
                end;
                begin
                    v_test_value_id := v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_id;
                exception
                when no_data_found then
                    raise_application_error(-20009,'result_'||substr('00'||v_i,-3)||' = '||v_result||' is incorrect.');
                end;
                if (v_test_step_status is null)
                then
                    raise_application_error(-20010,'result_'||substr('00'||v_i,-3)||' = '||v_result||' is incorrect.');
                end if;
                v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_result_id := null;
                v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).status               := v_test_value_status;
                v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).result               := v_test_value_result;
            end if;
        end if;
    end loop;

    select value_as_number into v_db_id from preference_value where lower(key) = 'dbid';

-- product: use existing one or create new
    begin
        select id into v_product_id from product where wabco_part_id = v_wabcopart_id and serial_number = v_serial_number;
    exception
    when no_data_found then
        v_product_id := null;
    end;
    if (v_product_id is null)
    then
        v_product_id := product_seq.nextval;
        insert into product (id,           db_id,   l_id,         wabco_part_id,  customer_id, cr_time,              md_time,                                      individual, serial_number,   xcomment,   archive)
        values              (v_product_id, v_db_id, v_product_id, v_wabcopart_id, 1,           v_process_start_time, nvl(v_process_start_time,v_process_end_time), 1,          v_serial_number, v_xcomment, '0');
    else
        update product set
            md_time = nvl(v_process_start_time,v_process_end_time),
            xcomment = v_xcomment
        where
            id = v_product_id and
            (
                nvl(md_time,to_date('2000-01-02 03:04:05','YYYY-MM-DD HH24:MI:SS')) != nvl(v_process_start_time,v_process_end_time) or 
                nvl(xcomment,'xabcxabcxabc') != nvl(v_xcomment,'xabcxabcxabc')
            );
    end if;

-- process_result: use existing one or create new
    begin
        select id into v_process_result_id from process_result where process_id = v_process_id and product_id = v_product_id;
    exception
    when no_data_found then
        v_process_result_id := null;
    end;
    if (v_process_result_id is null)
    then
        v_process_result_id := process_result_seq.nextval;
        insert into process_result(id,                  db_id,   l_id,                process_id,   product_id,   status_id,               start_time,           end_time,           archive)
        values                    (v_process_result_id, v_db_id, v_process_result_id, v_process_id, v_product_id, nvl(v_process_status,2), v_process_start_time, v_process_end_time, '0');
    else
        update process_result set
            status_id = nvl(v_process_status,status_id),
            start_time = v_process_start_time,
            end_time = v_process_end_time
        where
            id = v_process_result_id
            and
            (
                nvl(status_id,10000) != nvl(v_process_status,10000) or
                nvl(start_time,to_date('2000-01-02 03:04:05','YYYY-MM-DD HH24:MI:SS')) != nvl(v_process_start_time,to_date('2000-01-02 03:04:05','YYYY-MM-DD HH24:MI:SS')) or
                nvl(end_time,to_date('2000-01-02 03:04:05','YYYY-MM-DD HH24:MI:SS')) != nvl(v_process_end_time,to_date('2000-01-02 03:04:05','YYYY-MM-DD HH24:MI:SS'))
            );
    end if;

-- process_step_result: create new
    v_process_step_result_id := process_step_result_seq.nextval;
    insert into process_step_result (id,                       db_id,   l_id,                     process_result_id,   process_step_id,   status_id,             operator_id,   start_time,                end_time,                archive)
    values                          (v_process_step_result_id, v_db_id, v_process_step_result_id, v_process_result_id, v_process_step_id, v_process_step_status, v_operator_id, v_process_step_start_time, v_process_step_end_time, '0');
    
-- test_step_result and test_value_result in loop
    v_test_order := v_test_step_tbl.first;
    while (v_test_order is not null)
    loop
        v_test_step_status := v_test_step_tbl(v_test_order).status;
        if (v_test_step_status is not null)
        then
            v_test_step_id := v_test_step_tbl(v_test_order).test_step_id;
            v_test_step_result_id := test_step_result_seq.nextval;
            v_test_step_tbl(v_test_order).test_step_result_id := v_test_step_result_id;
            insert into test_step_result (id,                    db_id,   l_id,                  process_step_result_id,   test_step_id,   status_id,          archive)
            values                       (v_test_step_result_id, v_db_id, v_test_step_result_id, v_process_step_result_id, v_test_step_id, v_test_step_status, '0');
            v_test_value_sequence := v_test_step_tbl(v_test_order).test_value_tbl.first;
            while (v_test_value_sequence is not null)
            loop
                v_test_value_status := v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).status;
                if (v_test_value_status is not null)
                then
                    v_test_value_id := v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_id;
                    v_test_value_result := v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).result;
                    v_test_value_result_id := test_value_result_seq.nextval;
                    v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_result_id := v_test_value_result_id;
                    insert into test_value_result (id,                     db_id,   l_id,                   test_step_result_id,   test_value_id,   status_id,           result,              archive, version)
                    values                        (v_test_value_result_id, v_db_id, v_test_value_result_id, v_test_step_result_id, v_test_value_id, v_test_value_status, v_test_value_result, '0',       0);
                end if; 
                v_test_value_sequence := v_test_step_tbl(v_test_order).test_value_tbl.next(v_test_value_sequence);
            end loop;
        end if;
        v_test_order := v_test_step_tbl.next(v_test_order);
    end loop;
/*
    dbms_output.put_line('v_wabcopart_id:'||v_wabcopart_id);
    dbms_output.put_line('v_process_id:'||v_process_id);
    dbms_output.put_line('v_process_step_id:'||v_process_step_id);
    dbms_output.put_line('v_product_id:'||v_product_id);

    v_test_order := v_test_step_tbl.first;
    while (v_test_order is not null)
    loop
        dbms_output.put_line('v_test_order: '||v_test_order);
        dbms_output.put_line('-test_step_id: '||v_test_step_tbl(v_test_order).test_step_id);
        dbms_output.put_line('-test_step_result_id: '||v_test_step_tbl(v_test_order).test_step_result_id);
        dbms_output.put_line('-status: '||v_test_step_tbl(v_test_order).status);
        v_test_value_sequence := v_test_step_tbl(v_test_order).test_value_tbl.first;
        while (v_test_value_sequence is not null)
        loop
            dbms_output.put_line('-v_test_value_sequence '||v_test_value_sequence);
            dbms_output.put_line('--test_value_id: '||v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_id);
            dbms_output.put_line('--test_value_result_id: '||v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).test_value_result_id);
            dbms_output.put_line('--status: '||v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).status);
            dbms_output.put_line('--result: '||v_test_step_tbl(v_test_order).test_value_tbl(v_test_value_sequence).result);
            v_test_value_sequence := v_test_step_tbl(v_test_order).test_value_tbl.next(v_test_value_sequence);
        end loop;
        v_test_order := v_test_step_tbl.next(v_test_order);
    end loop;
*/
end;
/
