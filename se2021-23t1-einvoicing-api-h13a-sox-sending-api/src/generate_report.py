"""
Generate Report
Filename: generate_report.py

Author: James, Jacqueline
Created: 11/03/2023

Description: Generates a status report and stores it in
the database
"""

import datetime
from data_base import data_base

def generate_report(sender, recipient, description, errors):
    store = data_base.get()
    reports = store['communication_reports']

    if errors == {}:
        status = "Successful"
    else:
        status = "Unsuccessful"

    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y, %H:%M:%S")

    report = {
        "date": date,
        "sender": sender,
        "recipient": recipient,
        "description": description,
        "status": status
    }

    report_id = len(reports)
    reports[report_id] = report
    store['reports'] = reports
    data_base.set(store)

    return report_id
