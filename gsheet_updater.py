#!/bin/python

import gspread
from google.oauth2.service_account import Credentials
import json
#from autoqc.admin import AdminActions
from menu import Prompt
import sys


'''
Version to push to GitHub
'''


# Get values of a cell, print val if not == None
column_1 = 'B'
column_2 = 'C'

scopes = ["https://www.googleapis.com/auth/spreadsheets"] # This is the scope that allows us to read and write to Google Spreadsheets
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) # this just creates a variable in the correct format to allow for authentication
client = gspread.authorize(creds)  #  This uses the creds variable to authenticate into the Google Sheets API acct

sheet_id = "{SHEET-ID}" # To get this goto sheet URL, it is between '/d/' and '/edit?'
sheet = client.open_by_key(sheet_id) # Тhis is the Google Sheet as an object
Spreadsheet = type(sheet)

def open_json_data(filename):
    '''
    for reading from a JSON file (might be unnecessary here)
    '''
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
        #redundant to loop through or write to another dict since json.load
        #treats json data as python dict type
    return data

def worksheet_menu(worksheet):
    '''
    Taking the worksheet list from the get_worksheet func and using it to populate
    a terminal menu so that the worksheet can be selected from easily
    '''
    options = {}
    # Put the Sheet option above the exit option
    options.update({'Sheets' : [*worksheet]}) 
    options.update({"Exit" : sys.exit})  
    # sending the options to the menu handler that returns the selection made back
    selection = Prompt.dict_menu(options)  
    if selection == 'Exit': 
        print('Exiting...')
    if selection == 'Sheets':
        selection = Prompt.term_menu(options['Sheets'])
        print(
            f'You selected sheet: {selection}\n'
            f'Writing data to {selection}...'
              )
        return selection

def get_worksheet(sheet):
    '''
    Using the sheet object, getting a list of the worksheets on the Google Sheets 
    accessed. This returns as a class list object. Then using the gspread built-in
    worksheet title variable, iterate through each item in the worksheet_obj to get
    a clean list of worksheet names, this is then sent to the worksheet_menu func,
    which in gives us the worksheet selected, which is then return
    '''
    worksheet_obj = sheet.worksheets()
    size = len(worksheet_obj)
    ws = []
    for i in range(size):
        ws.append(worksheet_obj[i].title)
    worksheet = worksheet_menu(ws)
    return worksheet

def get_first_empty(col_num : int, sh):
    '''
    Using gspread's built-in return all values in a column method, or col_values, 
    I can avoid iterating through each cell in a column (which ends up making a 
    lot of requests to the Google Sheet), I can just get all the values, and then add
    1 to the length/size of the returned list to get the next empty cell (because the
    method only gives us the cells that have values inputted in them)
    '''
    ws = sheet.worksheet(sh)
    col_vals = ws.col_values(col_num)
    empty = len(col_vals) + 1
    return empty

def updater(row : int, col0 : str, col1 : str, data : dict, sh):
    '''
    Updates cells using columns and row numbers (starting at the first empty given by 
    get_first_empty), with JSON data (key,val) using the name of the selected worksheet
    from get_worksheet and worksheet_menu
    '''
    ws = sheet.worksheet(sh)
    for key,val in data.items():
        ws.update_acell(col0+str(row), key)
        ws.update_acell(col1+str(row), val)
        row += 1 
    
if __name__ == '__main__':
    sh = get_worksheet(sheet)
    empty = get_first_empty(2, sh)
    #jsondata = open_json_data('data.json')
    driver = webdriver.Chrome()
    actions = AdminActions(driver)
    actions.login('your_username', 'your_password')

    serials = actions.get_input_serials()
    serials_to_data = {}

    for serial in serials:
        try:
            data = actions.search(serial)
            serials_to_data[serial] = data
        except:
            continue
    jsondata = json.dumps(serials_to_data, indent=4)
    print(jsondata)
    updater(empty, column_1, column_2, jsondata, sh)
