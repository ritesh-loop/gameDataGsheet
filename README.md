# gameDataGsheet
Containing data related to various games online in IGDB

This project has 2 data-gathering parts -
1. using the IGDB API endpoint - ```https://api.igdb.com/v4/games``` and write to the gsheet.
2. Using Beautiful Soup to crawl the web, extract the genre, and write to the gsheet.

To gather data from the API into the gsheet run - ```python3 sheetWriter.py```

To scrap genre data from the IGDB game website and insert it into gsheet run - ```python3 IGDBGenreScrapper.py```

Endpoints at - https://api-docs.igdb.com/#endpoints

Gsheet Link - https://docs.google.com/spreadsheets/d/1IMvAoJnfVJdBfdfCokS_PBYVM8mq1xbFtBephK2tUYc/edit?usp=sharing

-------------------------------------------------------------------------------------------------------------------------------------------------------

Created an API under the folder gameDataAPI, this API is exposed with the collected data from above.
API route - ```http://127.0.0.1:8000/game-data/?game_id=```
```game_id``` - a query parameter, that takes the unique ID for every game in the IGDB database.
The response of this API returns - the game data present in the sheet.
Run the mains.py app > ```uvicorn mains:appName --reload```
Follow the link for the localhost and ```http://127.0.0.1:8000/docs``` to test the APIs with swagger UI

git handling - 
git status
git push
https://chat.openai.com/share/93fe312e-6290-4d59-85b8-0d14e3032037
https://gist.github.com/mindplace/b4b094157d7a3be6afd2c96370d39fad
