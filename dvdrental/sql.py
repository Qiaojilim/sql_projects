#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 09:36:38 2022

@author: qiaojixu
"""
##interact with a database in PostgreSQl with Python.
import psycopg2 as pg2

"""Making the initial connection: """
secret = 'password'
#conn = pg2.connect(database='dvdrental',user='postgres', password=secret)
try:
    conn = pg2.connect(database='dvdrental', user='postgres', host='localhost', password=secret)
except:
    print ("I am unable to connect to the database")

##define a cursor to work with
cur = conn.cursor()

##we can execute a query: pass any string operations of SQL in Python
cur.execute('SELECT * FROM payment')

#When you have executed your query you need to have a list [variable?] to put your results in.
##return first row of data
cur.fetchone() 
#return the first 10 colms
cur.fetchmany(10) ##return a list
cur.fetchall()

data = cur.fetchmany(10)
data[0][2]


conn.close()


command = 'SELECT * FROM payment'
cur.execute(command)

