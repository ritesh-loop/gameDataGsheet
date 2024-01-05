import gspread
from gameGenrePredictor import game_data_for_id
from ratelimit import limits, sleep_and_retry
import os
import csv
import re


def connecting_to_worksheet():
    Sheet_credential = gspread.service_account("/Users/riteshmukhopadhyay/Documents/Data Analysis/NLP/gameGenrePredictor/vernal-maker-382315-37af6c1e1384.json")
    # Open Spreadsheet by URL
    #spreadsheet = Sheet_credential.open_by_url('https://docs.google.com/spreadsheets/d/1IMvAoJnfVJdBfdfCokS_PBYVM8mq1xbFtBephK2tUYc/edit#gid=0')
    
    # Open Spreadsheet by key
    spreadsheet = Sheet_credential.open_by_key('1IMvAoJnfVJdBfdfCokS_PBYVM8mq1xbFtBephK2tUYc')

    # to print worksheet name using sheet id
    worksheet = spreadsheet.get_worksheet(0)
    
    # to print worksheet name using sheet name
    #worksheet = spreadsheet.worksheet('gameBotData')
    print("Connection established, Worksheet connected to - Title: {}, Worksheet_name:{}".format(spreadsheet.title,worksheet.title))
    return worksheet

# https://stackoverflow.com/a/54492234/10990865 > Gsheet Doc
# Define the rate limit: Write requests per minute per user is 60
@sleep_and_retry
@limits(calls=1, period=1.5)
def WriteRequestsGsheet(row,worksheet):
    worksheet.append_row(row)


def receiveDataFromIgdbAPI(data_received,total_length,worksheet):
    # Append each row of data to the sheet
    for row in data_received:
        WriteRequestsGsheet(row,worksheet)
    print(f"Write done of {total_length} data's in {worksheet}")
    

# Appending the data in gsheet
def genreAppenderInGsheet(genre_each_game="NA",GenreSheet=""):
    genres_together = ""
    append_column_name = 'genre'
    genre_column_index = GenreSheet.find(append_column_name).col  # Find the column number by column name
    # Find the first empty cell in the 'genre' column
    genre_column = GenreSheet.col_values(genre_column_index)
    #empty_cell_index = genre_column.index('') + 1 if '' in genre_column else len(genre_column) + 1
    empty_cell_index = next((i for i, val in enumerate(genre_column) if val == ''), len(genre_column) + 1)
    print(f"First Empty Cell present in Genre col - {empty_cell_index}")
    # Update the 'genre' column at the empty cell
    for genre in genre_each_game:
        genres_together = genres_together + genre + ","
    print(f"genres together {genres_together}")
    if re.match(r'^-*(,-*-*)*$', genres_together):
        # Running a condition if all characters are "-"
        print("All characters in the string are '-,'")
        genres_together = "-"
        GenreSheet.update_cell(empty_cell_index, genre_column_index, genres_together)
        print(" -- No Genre Appended 📝 {}".format(genres_together))
    else:
        GenreSheet.update_cell(empty_cell_index, genre_column_index, genres_together.replace("-", "").strip(","))
        print(" -- Genre Appended 📝 {}".format(genres_together.replace("-", "").strip(",")))


if __name__ == "__main__":
    sheet_to_be_written = connecting_to_worksheet()
    gsheet_last_updated_game_id = 0
    # Writing games data to sheet
    # Define headers
    headers = ["id", "name", "storyline", "url","genre"]
    last_row_index = len(sheet_to_be_written.col_values(1))  # Assuming column A has continuous data
    # to check the sheets last entry is greater than 1, then pick the last entry of column 1 else push the headers
    if sheet_to_be_written.row_values(1) == headers and last_row_index > 1:
        # Get the values of the last row
        last_row_values = sheet_to_be_written.row_values(last_row_index)
        gsheet_last_updated_game_id = int(last_row_values[0])
        print(f"Last row data: {last_row_values}")
    else:
        # Write headers to the sheet if sheet is empty, Insert at the first row
        print("The sheet is empty. Inserting headers")
        sheet_to_be_written.insert_row(headers, index=1)

    # calling game_data_for_id() from gameGenrePredictor.py to update the gsheet data
    data_received, total_length = game_data_for_id(gsheet_last_updated_game_id+1) # received the full data
    receiveDataFromIgdbAPI(data_received,total_length,sheet_to_be_written)
