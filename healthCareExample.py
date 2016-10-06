# -*- coding: utf-8 -*-
"""
Created by Efron Licht

healthCareExample.py takes a CSV of in-hospital transfers and finds
patients who are 'frequent fliers' in and out of an ICU - i.e, they have left
and then return within 24 hours. 

input: CSV or Excel file with rows in the form 
(NAME/TYPE):
    'NAME'/str, 'DEPT-FROM'/str, 'DEPT-TO'/str, 'TIME'/<datetime>

output: CSV with rows in the form
(NAME/TYPE):
    'NAME'/str, 'IN'<datetime>, 'OUT'<datetime>

"""
from collections import namedtuple
import csv
import datetime

""" 
helper functions start here
"""

def import_transfers(filename):
    """ import transfers from CSV, convert to namedtuple, then read into memory """
    Transfer = namedtuple('Transfer', ['name', 'isFrom', 'to', 'time'])
    with open(filename) as file:
        database = csv.reader(file)
        transfers = [Transfer(*line) for line in database]
        return transfers

def generate_frequent_fliers(transfers):
    """ generator function that yields patients who have transferred
    out of ICU, and then return within 24 hours"""
    FrequentFlier = namedtuple('FrequentFlier', ['name', 'left', 'returned'])
    TWENTY_FOUR_HOURS = datetime.timedelta(seconds = 60) * 60 * 24
    seen = {}
    for transfer in transfers:
        patient = transfer.name
        if transfer.isFrom == 'ICU':
            seen[patient] = transfer
            # because of our sort, this is always the most recent transfer out time
        elif patient in seen and transfer.to == 'ICU':
            departed = seen[patient].isFrom
            returned = transfer.to
            if returned.time - departed.time < TWENTY_FOUR_HOURS:
                yield FrequentFlier(patient, departed.time, returned.time)

def export_frequent_fliers(OUTPUT_FILEPATH, frequentFliers):
    """ writes list of frequent_fliers as CSV to output file in the following form:
    NAME, TIME IN, TIME OUT """
    with open(OUTPUT_FILEPATH, 'w') as file:
        writer = csv.writer(file)
        for frequentFlier in frequentFliers:
            writer.writerow(frequentFlier)

"""
helper functions end here
"""

""" this is what actually runs """
INPUT_FILEPATH = 'testin.csv'
OUTPUT_FILEPATH = 'testout.csv'
transfers = import_transfers(INPUT_FILEPATH)
transfers = sorted(transfers, key = lambda x: x.time)
frequentFliers = generate_frequent_fliers(transfers)
export_frequent_fliers(OUTPUT_FILEPATH, frequentFliers)
