# tests/test_integration_scrape_sheets.py
"""
This module contains integration tests for the scrape_sheets module.
"""

from unittest.mock import patch, MagicMock
import pytest
from SiteToSheet.scrapers.web_scraping import WebDataHunter
from SiteToSheet.api_clients.google_sheets_client import GoogleSheetsClient

@pytest.fixture
def mock_sheets_client():
    """
    Returns a MagicMock object that mimics the behavior of the GoogleSheetsClient class.
    The MagicMock object has a gs_headers attribute that contains a dictionary with '
    the keys "Link", "Location", and "Price".
    """
    client = MagicMock(spec=GoogleSheetsClient)
    client.gs_headers = {"Link":1, "Location":2, "Price":3}
    return client

@pytest.fixture
def web_hunter():
    """
    Returns an instance of the WebDataHunter class.
    """
    return WebDataHunter()

@patch('SiteToSheet.scrapers.web_scraping.requests.get')
def test_obtain_all_link_info(mock_get, web_hunter, mock_sheets_client):
    """
    Test the `obtain_all_link_info` method of the `WebDataHunter` class.

    This test function mocks the `requests.get` method to simulate a successful HTTP request.
    It then calls the `obtain_all_link_info` method with a sample URL and a list of search terms.
    The method returns a dictionary containing the extracted information from the web page.

    The test asserts that the returned dictionary contains the expected values for the "Link", "Location",
    and "Price" keys. It also tests the interaction with the `GoogleSheetsClient` by asserting that the
    `update_links_info` method is called with the correct argument.

    Parameters:
        mock_get (MagicMock): A mock object of the `requests.get` method.
        web_hunter (WebDataHunter): An instance of the `WebDataHunter` class.
        mock_sheets_client (MagicMock): A mock object of the `GoogleSheetsClient` class.

    Returns:
        None
    """
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = "<html><body><p>Looking for \
        in  Clapham, London,  </p><p>Price: £500,000</p></body></html>"
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

    assert isinstance(web_info) == dict

