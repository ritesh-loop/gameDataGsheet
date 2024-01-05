from gameGenrePredictor import IgdbScrapper
from sheetWriter import connecting_to_worksheet, genreAppenderInGsheet

sheet_to_be_read = connecting_to_worksheet()

# Reading sheet url col
def gsheet_url_reader(worksheet):
    genreList = []
    column_to_read = 4
    # Read values from the chosen column until the last non-empty cell
    IgdbLinkList = worksheet.col_values(column_to_read)[1:]# Skip the first row (header)

    print(f"First Link  - {IgdbLinkList[0]},Last Link -{IgdbLinkList[len(IgdbLinkList)-1]}")
    print("^"*60)
    print(f'toatal length of the extracted data from gsheet - {len(IgdbLinkList)}')
    genreList.append(Genre_extractor(IgdbLinkList,worksheet))
    print(genreList)


def readingTheLastDataInGenreColumn():
    all_genre_values = sheet_to_be_read.col_values(sheet_to_be_read.find('genre').col)
    genre_column_length = len(all_genre_values) - all_genre_values.count('')  # Exclude empty cells from count
    column_no = sheet_to_be_read.find('url').col
    row_to_fetch = genre_column_length  # Fetch value at the determined length
    url_cell_value = sheet_to_be_read.cell(row_to_fetch, column_no).value
    print(f"URL - {url_cell_value} already updated with genre")
    return url_cell_value


def Genre_extractor(Igdb_web_urls,worksheet):
    last_updated_genre_cell_value_url = readingTheLastDataInGenreColumn()
    if last_updated_genre_cell_value_url in Igdb_web_urls:
        position = Igdb_web_urls.index(last_updated_genre_cell_value_url) # Get the index of 'url'
        print(f"{last_updated_genre_cell_value_url} found at position: {position+2} in gsheet")
    else:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{last_updated_genre_cell_value_url} not found in the listiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    next_url_in_gsheet = position+1
    for link in Igdb_web_urls[next_url_in_gsheet:]:
        result = []
        print("-"*70)
        print(link)
        genre = IgdbScrapper(link)
        string_genre_list = [str(item) for item in genre]
        # Define the substring to search for
        substring = "genres"
        # Iterate through the list
        for item in string_genre_list:
            if substring in item:
                split_by_genres = item.split('/genres/')[1:]
                for final_item in split_by_genres:
                    start = final_item.find('">')  # Find the start index of the substring
                    end = final_item.find('</a>')  # Find the end index of the substring
                    if start != -1 and end != -1:
                        substring = final_item[start + 2:end]  # Extract the substring between '">' and '</a>'
                        result.append(substring.strip())
            else:
                result.append("-")
        print("printing this {}".format(result)) # here data will be appended to the same gsheet mapped with url
        genreAppenderInGsheet(genre_each_game=result,GenreSheet=worksheet)
    return result


if __name__ == "__main__":
    print("Nice👌")
    gsheet_url_reader(sheet_to_be_read)
