"""
database storage connector
Filename: database_storage_connector.py

Author: Nathan
Created: 14/04/2023

Description: database invoice storage connector between python and mysql
"""
import mysql.connector
# establish a connection to the database
mydb = mysql.connector.connect(
    user='root',
    password='Zyq021113!',
    host='localhost',
    database='invoice_storage',
    port='3306'
)
# create a cursor object
mycursor = mydb.cursor()

# select data from users table
mycursor.execute('SELECT*FROM users')

users = mycursor.fetchall()
print("users data:")
for result in users:
    print(result)


# select data from reset_codes table
mycursor.execute('SELECT*FROM reset_codes')

reset_codes = mycursor.fetchall()
print("\nreset_codes data:")
for result in reset_codes:
    print(result)


# select data from invoices table
mycursor.execute('SELECT*FROM invoices')

invoices = mycursor.fetchall()
print("\ninvoices data:")
for result in invoices:
    print(result)

# close the cursor and database connection
mycursor.close()
mydb.close()
