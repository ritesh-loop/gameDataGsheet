# gameDataGsheet
Containing data related to various games online in IGDB

This project has 2 data-gathering parts -
1. using the IGDB API endpoint - ```https://api.igdb.com/v4/games``` and write to the gsheet.
2. Using Beautiful Soup to crawl the web, extract the genre, and write to the gsheet.

To gather data from the API into the gsheet run - ```python3 sheetWriter.py```

To scrap genre data from the IGDB game website and insert it into gsheet run - ```python3 IGDBGenreScrapper.py```

Endpoints at - https://api-docs.igdb.com/#endpoints

git handling - 

https://chat.openai.com/share/93fe312e-6290-4d59-85b8-0d14e3032037
https://gist.github.com/mindplace/b4b094157d7a3be6afd2c96370d39fad
