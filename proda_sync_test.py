#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cx_Oracle
db_connection_string = 'prodang/wabco@PT'

connection = cx_Oracle.connect(db_connection_string)
cursor = connection.cursor()

sql = """insert into product (serial_number) values('123')"""
try:
    cursor.execute(sql)
except cx_Oracle.IntegrityError as e:
    print e

connection.close()