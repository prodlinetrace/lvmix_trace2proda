/*
wybieranie kompletnej schemy dla wabco_number: 4640061000
*/

select
wabcopart.wabco_number,
process.id process_id,
process_step.id process_step_id,
process_step.process_sequence process_step_sequence,
systems.name,
test_step.test_sequence,
test_step.test_order,
nvl(ls_ts_3.lookup_text,ls_ts_0.lookup_text) ts_description,
test_value.test_value_sequence,
test_value.minimum,
test_value.maximum,
nvl(ls_tv_3.lookup_text,ls_tv_0.lookup_text) tv_description
from
    wabcopart
    join wabcopart_process on wabcopart.id = wabcopart_process.wabco_part_id
    join process on wabcopart_process.process_id = process.id
    join process_step on process.id = process_step.process_id
    join systems on process_step.system_id = systems.id
    join test_step on process_step.id = test_step.process_step_id
    join test_value on test_step.id = test_value.test_step_id
    left outer join language_strings ls_ts_3 on test_step.description_label = ls_ts_3.label and ls_ts_3.language_id=3
    left outer join language_strings ls_ts_0 on test_step.description_label = ls_ts_0.label and ls_ts_0.language_id=0
    left outer join language_strings ls_tv_3 on test_value.description_label = ls_tv_3.label and ls_tv_3.language_id=3
    left outer join language_strings ls_tv_0 on test_value.description_label = ls_tv_0.label and ls_tv_0.language_id=0
where
    wabcopart.wabco_number like '4640061000'
    and systems.name like 'LV_MIX%'
    and systems.name not like 'LV_MIX_process'
    and process.release_id = 1
    and process_step.release_id = 1
    and test_step.release_id = 1
    and test_value.release_id = 1
	order by wabcopart.wabco_number, process_step.process_sequence, test_step.test_sequence, test_step.test_order, test_value.test_value_sequence
    /*
    and process_step.process_sequence=32 
    */


/*
wybieranie definicji dla danego numeru wabco i process_step.process_sequence
opcjonalnie mo¿na zakomentowa wiersz "and process_step.process_sequence=14" aby wybra wszystkie process_step_sequence
*/

select
wabcopart.wabco_number,
process.id process_id,
process_step.id process_step_id,
process_step.process_sequence process_step_sequence,
systems.name,
test_step.test_sequence,
test_step.test_order,
nvl(ls_ts_3.lookup_text,ls_ts_0.lookup_text) ts_description,
test_value.test_value_sequence,
test_value.minimum,
test_value.maximum,
nvl(ls_tv_3.lookup_text,ls_tv_0.lookup_text) tv_description
from
    wabcopart
    join wabcopart_process on wabcopart.id = wabcopart_process.wabco_part_id
    join process on wabcopart_process.process_id = process.id
    join process_step on process.id = process_step.process_id
    join systems on process_step.system_id = systems.id
    join test_step on process_step.id = test_step.process_step_id
    join test_value on test_step.id = test_value.test_step_id
    left outer join language_strings ls_ts_3 on test_step.description_label = ls_ts_3.label and ls_ts_3.language_id=3
    left outer join language_strings ls_ts_0 on test_step.description_label = ls_ts_0.label and ls_ts_0.language_id=0
    left outer join language_strings ls_tv_3 on test_value.description_label = ls_tv_3.label and ls_tv_3.language_id=3
    left outer join language_strings ls_tv_0 on test_value.description_label = ls_tv_0.label and ls_tv_0.language_id=0
where
    wabcopart.wabco_number like '4640061000'
    and systems.name like 'LV_MIX%'
    and process.release_id = 1
    and process_step.release_id = 1
    and test_step.release_id = 1
    and test_value.release_id = 1
    and process_step.process_sequence=14
    order by wabcopart.wabco_number, process_step.id, test_step.test_order, test_value.test_value_sequence
;



/*
wybieranie zapisanych wynikow ze wszystkich stacji dla danego numeru wabco i numeru seryjnego
*/
select
wabcopart.wabco_number,
process.id process_id,
process_step.id process_step_id,
process_step.process_sequence process_step_sequence,
systems.name,
test_step.test_sequence,
test_step.test_order,
nvl(ls_ts_3.lookup_text,ls_ts_0.lookup_text) ts_description,
test_value.test_value_sequence,
test_value.minimum,
test_value.maximum,
nvl(ls_tv_3.lookup_text,ls_tv_0.lookup_text) tv_description
,product.id product_id
,process_result.status_id process_result_status
,process_step_result.status_id process_step_result_status
,test_step_result.status_id test_step_result_status
,test_value_result.status_id test_value_result_status
,test_value_result.result result
from
    wabcopart
    join wabcopart_process on wabcopart.id = wabcopart_process.wabco_part_id
    join process on wabcopart_process.process_id = process.id
    join process_step on process.id = process_step.process_id
    join systems on process_step.system_id = systems.id
    join test_step on process_step.id = test_step.process_step_id
    join test_value on test_step.id = test_value.test_step_id
    left outer join language_strings ls_ts_3 on test_step.description_label = ls_ts_3.label and ls_ts_3.language_id=3
    left outer join language_strings ls_ts_0 on test_step.description_label = ls_ts_0.label and ls_ts_0.language_id=0
    left outer join language_strings ls_tv_3 on test_value.description_label = ls_tv_3.label and ls_tv_3.language_id=3
    left outer join language_strings ls_tv_0 on test_value.description_label = ls_tv_0.label and ls_tv_0.language_id=0
    join product on wabcopart.id = product.wabco_part_id 
    join process_result on product.id = process_result.product_id and process.id = process_result.process_id
    join process_step_result on process_result.id = process_step_result.process_result_id and process_step.id = process_step_result.process_step_id
    join test_step_result on process_step_result.id = test_step_result.process_step_result_id and test_step.id = test_step_result.test_step_id
    join test_value_result on test_step_result.id = test_value_result.test_step_result_id and test_value.id = test_value_result.test_value_id
where
    wabcopart.wabco_number like '4640061000'
    and product.serial_number = '108852'
    and process.release_id = 1
    and process_step.release_id = 1
    and test_step.release_id = 1
    and test_value.release_id = 1
    order by wabcopart.wabco_number, process_step.id, test_step.test_order, test_value.test_value_sequence
;


/*
przyk³adowy insert
*/

insert into
vw_test_lvmix(
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
   result_004,
   result_005,
   result_006,
   result_007,
   result_008,
   result_009,
   result_010,
   result_011,
   result_012,
   result_013,
   result_014,
   result_015,
   result_016,
   result_017
) values (
'4640061000',
14,
'108852',
'testowanie triggera',
to_date('2018-11-04 10:23:45','YYYY-MM-DD HH24:MI:SS'),
to_date('2018-11-04 10:33:50','YYYY-MM-DD HH24:MI:SS'),
null,
to_date('2018-11-04 10:25:00','YYYY-MM-DD HH24:MI:SS'),
to_date('2018-11-04 10:26:00','YYYY-MM-DD HH24:MI:SS'),
1,
334,
'TS_100_1',
'TV_100_1_1_1',
'TS_1410_1',
'TV_1410_1_1_47.58',
'TV_1410_2_1_258.77',
'TS_1420_1',
'TV_1420_1_1_0.096',
'TV_1420_2_1_2705',
'TV_1420_3_1_12.5',
'TS_1430_1',
'TV_1430_1_1_1.1123',
'TV_1430_2_1_2799.98',
'TV_1430_3_1_11.03',
'TS_1480_1',
'TV_1480_1_1_0.077',
'TV_1480_2_1_3200',
'TV_1480_3_1_15.5'
);

insert into
vw_test_lvmix(
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
   result_002
) values (
'4640061000',
23,
'108852',
'testowanie triggera',
to_date('2018-11-04 10:23:45','YYYY-MM-DD HH24:MI:SS'),
to_date('2018-11-04 10:33:50','YYYY-MM-DD HH24:MI:SS'),
null,
to_date('2018-11-04 10:25:00','YYYY-MM-DD HH24:MI:SS'),
to_date('2018-11-04 10:26:00','YYYY-MM-DD HH24:MI:SS'),
1,
334,
'TS_100_1',
'TV_100_1_1_1'
);


