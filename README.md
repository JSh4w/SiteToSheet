# SiteToSheet

SiteToSheet is a Python project that combines web scraping, natural language processing, and Google API integration to extract data from websites and store it in Google Sheets.

![python workflow](https://github.com/JSh4w/SiteToSheet/actions/workflows/python-package.yml/badge.svg)
[![Pylint](https://github.com/JSh4w/SiteToSheet/actions/workflows/pylint.yml/badge.svg)](https://github.com/JSh4w/SiteToSheet/actions/workflows/pylint.yml)

## Installation

This project requires Python 3.7 or later. To set up the project environment:

1. Clone the repository:
2. Create a virtual environment:
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required packages:
## Dependencies

This project relies on several key libraries:

- **Web Scraping**: BeautifulSoup4
- **Natural Language Processing**: spaCy (with en_core_web_sm model)
- **Google API Integration**: google-api-python-client, gspread
- **Data Manipulation**: pandas, numpy
- **Mapping**: googlemaps
- **Environment Management**: python-dotenv
- **Rate Limiting**: ratelimit

For a complete list of dependencies, see the `requirements.txt` file.

## Configuration

1. Set up Google Cloud Project and enable necessary APIs (Sheets, Maps):
   To do this follow the steps found here https://developers.google.com/sheets/api/quickstart/python#set-up-environment
   Complete the steps up to but not including "Install the Google Client Library" 
3. Create and download a `sheet_credentials.json` file for Google API authentication. It must be named sheet_credentials.
   Unlike the tutorial store this in your LocalAppData/SiteToSheet folder. If this is not present the package will ask for its creation
   Typically this resides at C:\Users\{user}\AppData\Local\SiteToSheet for Windows machines 
5. Create a `.env` file in the project root alongside your `sheet_credentials.json` and add your API keys:
![image](https://github.com/user-attachments/assets/6cc2695c-7f32-493d-a106-624d4bf7f815)

##Usage 

Once all credentials are present you can begin filling in your Google spreadsheet with the data you wish to search

#TODO include video of excel spreadsheet being filled in 

## Features

- Web scraping with BeautifulSoup4
- Natural language processing with spaCy
- Google Sheets integration for data storage
- Google Maps API for geolocation services
- Rate limiting to respect API usage limits

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project uses the following third-party services and libraries:

- Google Maps Distance Matrix API: Subject to the [Google Maps Platform Terms of Service](https://cloud.google.com/maps-platform/terms)
- Google Sheets API: Subject to the [Google APIs Terms of Service](https://developers.google.com/terms)
- spaCy: Licensed under the [MIT License](https://github.com/explosion/spaCy/blob/master/LICENSE)

Users of this software are responsible for ensuring their own compliance with the terms of these services and libraries.

## Acknowledgments

This project makes use of several open-source libraries and APIs. We thank the maintainers and contributors of these projects.
