"""
database connector
Filename: database_connector.py

Author: Nathan
Created: 24/03/2023

Description: database connector between python and mysql
"""

import mysql.connector
# establish a connection to the database
mydb = mysql.connector.connect(
    user='root',
    password='Zyq021113!',
    host='localhost',
    database='invoice_sending',
    port='3306'
)
# create a cursor object
mycursor = mydb.cursor()

# select data from communication_report table
mycursor.execute('SELECT*FROM communication_report')

communication_report = mycursor.fetchall()
print("Communication Report data:")
for result in communication_report:
    print(result)


# select data from email table
mycursor.execute('SELECT*FROM email')

email = mycursor.fetchall()
print("\nEmail data:")
for result in email:
    print(result)

# close the cursor and database connection
mycursor.close()
mydb.close()