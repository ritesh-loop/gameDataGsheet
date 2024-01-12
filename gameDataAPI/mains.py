from fastapi import FastAPI
from enum import Enum
import gspread


def connecting_to_worksheet():
    Sheet_credential = gspread.service_account("/Users/riteshmukhopadhyay/Documents/Data Analysis/NLP/gameGenrePredictor/vernal-maker-382315-37af6c1e1384.json")
    # Open Spreadsheet by key
    spreadsheet = Sheet_credential.open_by_key('1IMvAoJnfVJdBfdfCokS_PBYVM8mq1xbFtBephK2tUYc')
    # to print worksheet name using sheet id
    worksheet = spreadsheet.get_worksheet(0)
    # to print worksheet name using sheet name
    print("Connection established✴️, Worksheet connected to - Title: {}, Worksheet_name:{}".format(spreadsheet.title,worksheet.title))
    return worksheet,"connection successful!"


def gameID_binary_search(id_list,targetID):
    left, right = 0, len(id_list) - 1
    while left <= right:
        mid = (left + right) // 2
        # Check if the target is at the middle
        if id_list[mid] == targetID:
            return mid
        # If the target is greater, ignore left half
        elif id_list[mid] < targetID:
            left = mid + 1
        # If the target is smaller, ignore right half
        else:
            right = mid - 1
    # If the target is not found
    return -1

# TO reload this app use - uvicorn mains:appName --reload   --main - name of the file, app - name of this app
appName = FastAPI()

@appName.get("/")
@appName.get("/home")
async def root():
    return {"message": "Hello, the API is made to expose game related information as per game ID"}

@appName.get("/game-data/")
async def read_item(game_id: int = 0):
    sheet_to_be_read, connection_status= connecting_to_worksheet()
    # Fetch data from the worksheet and format it to return as JSON
    column_headers = sheet_to_be_read.row_values(1)
    all_id_from_gsheet = sheet_to_be_read.col_values(1)
    all_id_from_gsheet=list(map(int, all_id_from_gsheet[1:]))
    
    response_data = {
        "connection_status": connection_status,
        "totalGameDataPresent": len(all_id_from_gsheet),
        "gameID_gsheet_status": "",
        "row_data":{}
    }
    
    if game_id == 0:
        response_data['gameID_gsheet_status'] = "Enter game ID between 1 and 215711"
        return response_data
    else:
        id_status = gameID_binary_search(all_id_from_gsheet,game_id)
        # id_status returns -1 if id is not present in the gsheet
        if id_status != -1:
            try:
                # Find the index of the specified unique ID in the column
                index = all_id_from_gsheet.index(game_id)

                # Return the row number (1-based index)
                print(index + 1)
            except ValueError:
                # ID not found
                print(ValueError)

            response_data['gameID_gsheet_status'] = f"Element found at gsheet row position {index+2}"
            # Get all values in the specified row
            row_values = sheet_to_be_read.row_values(index+2)
            row_data = dict(zip(column_headers, row_values))
            response_data['row_data']=row_data
        else:
            response_data['gameID_gsheet_status'] = "Element not found in the list"
        return response_data
