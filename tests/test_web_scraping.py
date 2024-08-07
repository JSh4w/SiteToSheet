# tests/test_web_scraping.py
import pytest
from SiteToSheet.scrapers.web_scraping import WebDataHunter

def test_is_regex():
    """
    Test the `is_regex` method of the `WebDataHunter` class.
    This function creates an instance of the `WebDataHunter` class and tests the `is_regex` method with two different inputs: a regular expression pattern and a literal string. It asserts that the `is_regex` method returns `True` when given a regular expression pattern and `False` when given a literal string.
    Parameters:
        None
    Returns:
        None
    """
    hunter = WebDataHunter()
    assert hunter.is_regex(r'.*') is True
    assert hunter.is_regex('literal string') is False

def test_can_fetch():
    """
    Test the `can_fetch` method of the `WebDataHunter` class.
    This function creates an instance of the `WebDataHunter` class and tests the `can_fetch` method with a specific URL.
    It asserts that the `can_fetch` method returns `True` when given a valid URL.
    Parameters:
        None
    Returns:
        None
    """
    hunter = WebDataHunter()
    assert hunter.can_fetch('https://en.wikipedia.org/wiki/Web_scraping') is True
    # Add more test cases

def test_html_parser():
    """
    Test the `html_parser` method of the `WebDataHunter` class.
    This function creates an instance of the `WebDataHunter` class and tests the `html_parser` method with a specific URL.
    It asserts that the `html_parser` method returns a non-empty string when given a valid URL.
    Parameters:
        None
    Returns:
        None
    """
    hunter = WebDataHunter()
    assert hunter.html_parser('https://en.wikipedia.org/wiki/Web_scraping') != ''