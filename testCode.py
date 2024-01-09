import gspread
from gameGenrePredictor import game_data_for_id
from ratelimit import limits, sleep_and_retry


Sheet_credential = gspread.service_account("/Users/riteshmukhopadhyay/Documents/Data Analysis/NLP/gameGenrePredictor/vernal-maker-382315-37af6c1e1384.json")
 
# Open Spreadsheet by URL
spreadsheet = Sheet_credential.open_by_url('https://docs.google.com/spreadsheets/d/1IMvAoJnfVJdBfdfCokS_PBYVM8mq1xbFtBephK2tUYc/edit#gid=0')
 
# Open Spreadsheet by key
#spreadsheet = Sheet_credential.open_by_key('1IMvAoJnfVJdBfdfCokS_PBYVM8mq1xbFtBephK2tUYc')
print(spreadsheet.title)

# to print worksheet name using sheet id
worksheet = spreadsheet.get_worksheet(0)

column_to_read = 4 # url column

# Scraping IGDB website to get genres after reading url column from gsheet
# Reading sheet url col



# Function to get the length of a specific column
def get_column_length(worksheet,column_name):
    values = worksheet.col_values(worksheet.find(column_name).col)
    length = len(values) - values.count('')  # Exclude empty cells from count
    return length

# Read values from the chosen column until the last non-empty cell
values = worksheet.col_values(column_to_read)
url_column_length = get_column_length(worksheet,column_name="url")
print(f"column length present in gsheet {url_column_length-1}")
print('--'*40)
print(f'toatal length of the extracted links from gsheet column url present in the list - {len(values)-1}')
print(values[1])
print(values[len(values)-1])

# Example column name to get the length
column_name = "genre"  # Replace with your column name

# Get the length of the specified column
genre_column_length = get_column_length(worksheet,column_name)
print(f"Length of '{column_name}' cells having actual data: {genre_column_length-1}")

print("-"*80)
print("exctracting the url as per the last updated genre cell...")

# Function to get the cell value for a specific row in a column
def get_last_cell_value_at_row(column_name, row):
    column = worksheet.find(column_name).col
    print(column)
    cell = worksheet.cell(row, column).value
    return cell

# Example column name and row to get the cell value
column_data_to_be_extracted_name = 'url'  # Replace with your column name
row_to_fetch = genre_column_length  # Fetch value at the determined length
print(row_to_fetch)
# Get the cell value at the specified row and column
cell_value = get_last_cell_value_at_row(column_data_to_be_extracted_name, row_to_fetch)
print(f"Value at row {row_to_fetch} in '{column_data_to_be_extracted_name}' column: {cell_value}")

if cell_value in values:
    position = values.index(cell_value)  # Get the index of 'cell_value'
    print(f"{cell_value} found at position: {position}")
else:
    print(f"{cell_value} not found in the list")

next_url_in_gsheet = values[position+1]

