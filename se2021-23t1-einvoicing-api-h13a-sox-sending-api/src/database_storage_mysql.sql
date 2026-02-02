"""
database invoice storage 
Filename: database_storage_mysql

Author: Nathan
Created: 14/04/2023

Description: Store the invoice data from the frontend into database and 
there are three tables users,reset_codes,invoices storing the data into mysql
"""
create schema invoice_storage;
use invoice_storage;

-- create table users
create table users (
user_id varchar(40),
user_name varchar(30),
last_name varchar(30),
email varchar(60),
user_password varchar(40),
sessions varchar(150)
);

-- create table reset_code
create table reset_codes(
user_id varchar(40)
);

-- create table invoices
create table invoices(
invoice_id varchar(40),
invoice_owner varchar(40),
created_date varchar(30),
the_data varchar(20),
deleted varchar(30)
);

