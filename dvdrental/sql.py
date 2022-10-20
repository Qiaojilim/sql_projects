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

## print all tables in this database
cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public' """)
for table in cur.fetchall():
    print(table)
##we can execute a query: pass any string operations of SQL in Python
# cur.execute('SELECT * FROM payment')

#When you have executed your query you need to have a list [variable?] to put your results in.
##return first row of data
# cur.fetchone() 
#return the first 10 colms
# cur.fetchmany(10) ##return a list
# cur.fetchall()
# data = cur.fetchmany(10)
# data[0][2]

"""
Module 1: basic sql operations to solve business analysis questions
"""

"1. Return the customer IDs of customers who have spent at least $110 with the staff member who has an ID of 2."
cur.execute('SELECT * FROM payment LIMIT 1')
##check columns names:
cur.description

cur.execute("""SELECT customer_id, SUM(amount) FROM payment
               WHERE staff_id = 2 
               GROUP BY customer_id
               HAVING SUM(amount) >= 110;
            """)

ans1 = cur.fetchall()
    
"2. How many films begin with the letter J?"    
cur.execute("SELECT * FROM film LIMIT 1")    
cur.description
cur.execute("""
            SELECT COUNT(*) FROM film
            WHERE title LIKE 'J%';
            """)     
ans2 = cur.fetchall()

"""
3. What customer has the highest customer ID number whose name starts with an 'E' 
and has an address ID lower than 500?
"""

cur.execute("SELECT * FROM customer LIMIT 1")    
cur.description
cur.execute("""
            SELECT first_name, last_name FROM customer
            WHERE first_name LIKE 'E%'
            AND address_id < 500
            ORDER BY customer_id DESC
            LIMIT 1;
            """)     
ans3 = cur.fetchall()

conn.close()


command = 'SELECT * FROM payment'
cur.execute(command)









