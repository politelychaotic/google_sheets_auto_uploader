#!/bin/python

import gspread
from google.oauth2.service_account import Credentials
import time
import json


'''
'''


# Get values of a cell, print val if not == None
column_1 = 'B'
column_2 = 'C'

scopes = ["https://www.googleapis.com/auth/spreadsheets"] # This is the scope that allows us to read and write to Google Spreadsheets
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) # this just creates a variable in the correct format to allow for authentication
client = gspread.authorize(creds)  #  This uses the creds variable to authenticate into the Google Sheets API acct

sheet_id = "{SHEET-ID}" # To get this goto sheet URL, it is between '/d/' and '/edit?'
sheet = client.open_by_key(sheet_id) 


def open_json_data(filename):
    #read json file
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
        #redundant to loop through or write to another dict since json.load
        #treats json data as python dict type
    return data

def get_date():
    pass

def get_first_empty(col_num : int):
    col_vals = sheet.sheet1.col_values(col_num)
    empty = len(col_vals) + 1
    return empty

def col_updater(row : int, col0 : str, col1 : str, data : dict):
    for key,val in data.items():
        sheet.sheet1.update_acell(col0+str(row), key)
        sheet.sheet1.update_acell(col1+str(row), val)
        row += 1 
    
if __name__ == '__main__':
    empty = get_first_empty(2)
    jsondata = open_json_data('data.json')
    col_updater(empty, column_1, column_2, jsondata)
