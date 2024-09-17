import gspread
from google.oauth2.service_account import Credentials
import time

scopes = ["https://www.googleapis.com/auth/spreadsheets"]    # This is the scope that allows us to read and write to Google Spreadsheets
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)    # JSON downloaded in creation of Google Sheets API to authenticate, 
                                                                                    # this just creates a variable in the correct format to allow for authentication
client = gspread.authorize(creds)    #  This uses the creds variable to authenticate into the Google Sheets API acct

sheet_id = "" # To get this goto sheet URL, it is between '/d/' and '/edit?'
sheet = client.open_by_key(sheet_id)

values_list = sheet.sheet1.row_values(1)    #   Just a test to show we are able to authenticate, and view cells in the sheet. Prints out headers
print(values_list)

col_0_data = [ # example data for filling out first column
    '1',
]
col_1_data = [ # example data for filling out second column
    '2',
]


# Get values of a cell, print val if not == None
column_1 = 'D'  # Placeholder column 0
column_2 = 'F' # Placeholder column 1

def find_empty_cells(col):
  '''
  Func to find the empty cells in a Google Sheets spreadsheet.
  :param col: The column (This is the letters at the top of the sheet)
  '''
    i = 2
    while True:
        cell_name = col + str(i)
        cell_val = sheet.sheet1.acell(cell_name).value
        if cell_val == None:
            print(cell_name)
            return cell_name
        
        i += 1
        time.time.sleep(0.25)  #  slow down requests because of rate limiting
        

def insert_data(cell_name, data):
  '''
  Func to insert data into a Google Sheets spreadsheet.
  :param cell_name: Takes the name of the first cell in the column that is empty (found using func find_empty_cells)
  :param data: The list name of the data that will be written in this column
  '''
    for i in range(len(data)):
        sheet.sheet1.update_acell(cell_name, data[i])

if __name__ == '__main__':
    col_0 = find_empty_cells(column_1)
    insert_data(str(col_0), col_0_data)
    col_1 = find_empty_cells(column_2)
    insert_data(str(col_1), col_1_data)
    print(col_0, col_1)
