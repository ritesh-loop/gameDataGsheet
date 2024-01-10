from fastapi import FastAPI
from enum import Enum
import gspread
from ratelimit import limits, sleep_and_retry



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

# TO reload this app use - uvicorn main:app --reload   --main - name of the file, app - name of this app
appName = FastAPI()

@appName.get("/")
@appName.get("/home")
async def root():
    return {"message": "Hello, the API is made to expose game related information as per game ID"}

@appName.get("/game-data/")
async def read_item(game_id: int = 0):
    sheet_to_be_written, connection_status= connecting_to_worksheet()
    # Fetch data from the worksheet and format it to return as JSON
    first_row_data = sheet_to_be_written.row_values(1)
    all_id_from_gsheet = sheet_to_be_written.col_values(1)
    all_id_from_gsheet=list(map(int, all_id_from_gsheet[1:]))
    
    response_data = {
        "connection_status": connection_status,
        "sheet_headers": first_row_data,
        "totalGameDataPresent": len(all_id_from_gsheet),
        "gameID_gsheet_status": ""
    }
    
    if game_id == 0:
        response_data['gameID_gsheet_status'] = "Enter game ID between 1 and 215711"
        return response_data
    else:
        # --- now making a binary search algorithm to find if the ID is present in all_id_from_gsheet
        id_status = gameID_binary_search(all_id_from_gsheet,game_id)
        if id_status != -1:
            response_data['gameID_gsheet_status'] = f"Element found at gsheet row position {id_status+1}"
        else:
            response_data['gameID_gsheet_status'] = "Element not found in the list"
        return response_data
