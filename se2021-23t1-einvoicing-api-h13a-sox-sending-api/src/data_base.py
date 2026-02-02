"""
Data Base
Filename: data_base.py

Author: Jacqueline
Created: 10/03/2023

Description: Stores all information in a database
dictionary
"""

initial_object = {
    'communication_reports': {}, # Empty dictionary for reports
    'emails': {}, # Empty dictionary for emails
    'users': {}, # Empty dictionary for users
    'reset_codes':{}, # Empty dictionary for reset codes
    'invoices': {} # Empty dictionary for invoices
}


class Database:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    # Saving new data to data base
    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


global data_base
data_base = Database()
