# tests/test_integration_scrape_sheets.py
import pytest
from unittest.mock import patch, MagicMock
from SiteToSheet.scrapers.web_scraping import WebDataHunter
from SiteToSheet.api_clients.google_sheets_client import GoogleSheetsClient

@pytest.fixture
def mock_sheets_client():
    client = MagicMock(spec=GoogleSheetsClient)
    client.gs_headers = {"Link":1, "Location":2, "Price":3}
    return client 

@pytest.fixture
def web_hunter():
    return WebDataHunter()

@patch('SiteToSheet.scrapers.web_scraping.requests.get')
def test_obtain_all_link_info(mock_get, web_hunter, mock_sheets_client):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = "<html><body><p>Looking for in  Clapham, London,  </p><p>Price: £500,000</p></body></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    #test
    url = "https://example.com/property"
    web_info = web_hunter.obtain_all_link_info(url, ["Location", "Price"])

    assert web_info["Link"] == url
    assert "London" in web_info["Location"]
    assert "Clapham" in web_info["Location"]
    assert "£500,000" in web_info["Price"]

    #Test interaction with GoogleSheets
    mock_sheets_client.update_links_info(web_info)
    mock_sheets_client.update_links_info.assert_called_with(web_info)

    assert type(web_info) == dict

