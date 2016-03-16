#!/usr/bin/env python
#-*- coding: utf-8 -*-
import logging
import sys
import os
import six
from trace2proda.models import *
import csv
from StringIO import StringIO
from sqlalchemy import or_



def main():
    #init_db()
    logger.info("Export Started")
    csv_header = ['Id', 'Type', 'Serial', 'Variant', 'Date Added', 'Week', 'Year', 'sila st 4.1 fitting 1', 'sila st 4.1 fitting 2', 'sila st 4.1 fitting 3', ' sila st 4.2 poz. 1', ' sila st 4.2 poz. 2', ' sila st 4.2 poz. 3']
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=',')
    writer.writerow(csv_header)
    products = Product.query.filter(or_(Product.type=='4640065200', Product.type=='4640065000') ).order_by(Product.date_added).limit(999999).all()
    for product in products:
        print product
        last_status = product.statuses.order_by(Status.id.desc()).first()
        row = ["{id}".format(id=product.id), "{type}".format(type=product.type), "{sn}".format(sn=product.serial), "{variant}".format(variant=product.variant.name), " {date}".format(date=product.date_added), "{week}".format(week=product.week), "{year}".format(year=product.year),]
        #row.append(product.operations.filter(Status.status==1))
        o_41_1 = product.operations.filter(Operation.operation_type_id==4110).first()
        o_41_2 = product.operations.filter(Operation.operation_type_id==4120).first()
        o_41_3 = product.operations.filter(Operation.operation_type_id==4130).first()
        o_42_1 = product.operations.filter(Operation.operation_type_id==14210).first()
        o_42_2 = product.operations.filter(Operation.operation_type_id==14220).first()
        o_42_3 = product.operations.filter(Operation.operation_type_id==14230).first()
        
        row.append(o_41_1.result_1) if o_41_1 else row.append(0)
        row.append(o_41_2.result_1) if o_41_2 else row.append(0) 
        row.append(o_41_3.result_1) if o_41_3 else row.append(0)
        row.append(o_42_1.result_1) if o_42_1 else row.append(0)
        row.append(o_42_2.result_1) if o_42_2 else row.append(0)
        row.append(o_42_3.result_1) if o_42_3 else row.append(0)
        writer.writerow(row)

    
    print buffer.getvalue()
    open("Piotr.Dyjur.export.csv", 'w').write(buffer.getvalue())
    logger.info("Export Finished")


if __name__ == "__main__":
    sys.exit(main())
