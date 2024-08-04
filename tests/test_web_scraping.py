# tests/test_web_scraping.py
import pytest
from SiteToSheet.scrapers.web_scraping import WebDataHunter

def test_is_regex():
    hunter = WebDataHunter()
    assert hunter.is_regex(r'.*') == True
    assert hunter.is_regex('literal string') == False

def test_can_fetch():
    hunter = WebDataHunter()
    assert hunter.can_fetch('https://en.wikipedia.org/wiki/Web_scraping') == True
    # Add more test cases

def test_html_parser():
    hunter = WebDataHunter()
    assert hunter.html_parser('https://en.wikipedia.org/wiki/Web_scraping') != ''