#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 09:36:38 2022

@author: qiaojixu
"""
##interact with a database in PostgreSQl with Python.
import psycopg2 as pg2

import pandas as pd
import pylab as pl

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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
sql =   """
        SELECT first_name, last_name FROM customer
        WHERE first_name LIKE 'E%'
        AND address_id < 500
        ORDER BY customer_id DESC
        LIMIT 1;
        """
cur.execute(sql)     
ans3 = cur.fetchall()


# "what range of a month, pay the most of money"
# sql = """
#       SELECT EXTRACT(DAY FROM payment_date) FROM payment
#       ORDER BY EXTRACT(DAY FROM payment_date);
#       """

# cur.execute(sql)   

# df = plt.read_sql(sql, conn)
# colors = ['aqua', 'red', 'gold', 'royalblue', 'darkorange', 'green']
# df.hist(bins=range(1, 32, 5), grid=False, color='#86bf91', sharex=True, zorder=2, rwidth=0.9)
# pl.title("Histogram of payment frequencies from customer table", fontweight="bold")
# pl.xlabel("Day")
# pl.ylabel("Payment Times")


# 

# cm = sns.color_palette("plasma",6) #Splitting the palette in the same amount of numbers bins
    
# # Plot histogram.
# plot = sns.histplot(data=df, x='extract', kde=True, bins=range(1, 32, 5))

# for bin_,i in zip(plot.patches,cm):
#     bin_.set_facecolor(i)
# plt.title("Histogram of payment frequencies from customer table", fontweight="bold")
# plt.xlabel("Day")
# plt.ylabel("Payment Times")

# plt.show()


# conn.close()



sql = """
   SELECT film.title film_title, category.name AS category_name, COUNT(rental.rental_date) rental_count
   FROM film 
   JOIN inventory 
     ON inventory.film_id = film.film_id
   JOIN rental 
     ON inventory.inventory_id = rental.inventory_id
   JOIN film_category 
     ON film.film_id = film_category.film_id
   JOIN category 
     ON film_category.category_id = category.category_id
 WHERE category.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family')	
 GROUP BY film_title, category_name
 ORDER BY rental_count DESC
 LIMIT 10;
 
 
 
      """

cur.execute(sql)   
colors = [ 'red', 'gold', 'royalblue', 'darkorange', 'green']

df = pd.read_sql(sql, conn)

fig = plt.figure()
# ax = plt.subplot(111)


sns.set_style("dark")
colours = {"Animation": "tab:blue", "Children": "tab:orange", "Classics":"tab:green", "Comedy":"tab:red", "Family":"tab:purple"}
ax = df.plot(x = 'film_title', y='rental_count',kind="barh",
        color=df['category_name'].replace(colours))



for i, v in enumerate(df['rental_count']):
    ax.text(v + 0.1, i + .05, str(v), color='grey', fontweight='bold')

plt.title("Top 10 family films based on rental count")
plt.xlabel("Rental Count")
plt.ylabel("Film Title")
plt.legend([Patch(facecolor=colours['Animation']),Patch(facecolor=colours['Children']),
            Patch(facecolor=colours['Classics']), Patch(facecolor=colours['Comedy']),
            Patch(facecolor=colours['Family'])], 
           
           
           
           ["Animation", "Children", "Classics", "Comedy", "Family"], bbox_to_anchor=(1.04, 1), borderaxespad=0,
           )


plt.savefig('foo.png', bbox_inches='tight', dpi=500)

#######################################################
#######################################################




    
    
    
    