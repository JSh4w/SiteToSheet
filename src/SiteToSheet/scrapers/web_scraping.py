"""Handles calls to web scrapers"""
from functools import wraps
from urllib import robotparser
from urllib.parse import urlparse
import re
import time
from ratelimit import limits, sleep_and_retry
import spacy
import requests
from bs4 import BeautifulSoup

class RateLimitExceededException(Exception):
    """Exception raised when the daily API request limit is exceeded."""

    def __init__(self, limit=20, message="Daily API request limit exceeded"):
        self.limit = limit
        self.message = f"{message}. Limit: {self.limit} requests per day."
        super().__init__(self.message)

class WebDataHunter:
    """
    A class for hunting web data.

    This class provides methods for scraping web pages and extracting data.
    """
    def __init__(self):
        """
        Initializes a WebDataHunter instance with default HTTP headers.
        
        The headers are set to mimic a Chrome browser on a Macintosh system, 
        which helps to avoid being blocked by websites that do not allow 
        scraping by default User-Agent headers.
        
        Parameters:
        None
        
        Returns:
        None
        """
        # Option 2: Using multiple lines for each key-value pair
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/71.0.3578.98 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/webp,image/apng,*/*;q=0.8"
        }
    def is_regex(self,pattern):
        """
        Checks if a given pattern is a regular expression.

        Parameters:
        pattern (str): The pattern to check.

        Returns:
        bool: True if the pattern is a regular expression, False otherwise.
        """
        # Check for common regex metacharacters
        regex_chars = set(r'.*+?^$()[]{}|\\')

        # If it contains regex metacharacters, it's likely a regex
        if any(char in regex_chars for char in pattern):
            return True

        # If it doesn't contain metacharacters, try to compile it as a regex
        try:
            re.compile(pattern)
            # If it compiles without error, it could be a simple regex or a string
            # We'll consider it a string in this case
            return False
        except re.error:
            # If it fails to compile, it's definitely not a valid regex
            return False

    @staticmethod
    def daily_limit(max_daily):
        """
        A decorator that limits the number of times a function can 
        be called within a 24-hour period.

        Parameters:
        max_daily (int): The maximum number of times the 
        function can be called within a 24-hour period.

        Returns:
        function: A decorator that wraps the original function and limits its calls.
        """
        def decorator(func):
            func.daily_count = 0
            func.last_reset = time.time()

            @wraps(func)
            def wrapper(*args, **kwargs):
                current_time = time.time()
                if current_time - func.last_reset >= 86400:  # 24 hours in seconds
                    func.daily_count = 0
                    func.last_reset = current_time

                if func.daily_count >= max_daily:
                    raise RateLimitExceededException(limit=max_daily)

                func.daily_count += 1
                return func(*args, **kwargs)
            return wrapper
        return decorator
    @staticmethod
    def can_fetch(url):
        """
        Checks if a given URL can be fetched based on the website's robots.txt rules.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL can be fetched, False otherwise.
        """
        rp = robotparser.RobotFileParser()
        parsed_uri = urlparse(url)
        domain = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        rp.set_url(f"{domain}/robots.txt")
        rp.read()
        return rp.can_fetch("*", url)

    #NLP process returns lists of list (text and the corresponding label)
    def nlp_process(self, text, labels) ->list:
        """
        Performs Natural Language Processing (NLP) on the given text to extract entities 
        that match the specified labels.

        Args:
            text (str): The text to process.
            labels (list): A list of labels to match.

        Returns:
            list: A list of lists containing the matched entity text and its corresponding label.
        """
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        matches=[]
        for ent in doc.ents:
            if ent.label_ in labels:
                matches.append([ent.text, ent.label_])
        return matches


    #Match via regex first then if not found use NLP for more accuracy
    def single_match_search(self, text, match):
        """
        Performs a single match search on the given text based on the provided match criteria.

        Args:
            text (str): The text to search in.
            match (str): The match criteria, which can be a string or a regular expression.

        Returns:
            str: The matched text if found, 
            otherwise an error message or the result of NLP processing.
        """
        if "(£)" in match or "Price" in match:
            successful_match =\
            [(match.group(), match.start()) for match in re.finditer(r'£\d{1,3},\d{1,3}', text)]
            if len(successful_match) == 0:
                return self.nlp_process(text, ["MONEY"])
            for i in successful_match:
                min_range = i[1]-30
                max_range = i[1]+30
                search_text = text[min_range:max_range]
                match=str(match).replace("(£)","")
                if match in search_text:
                    return i[0]
                return f"No {match} , found this value"+ str(i[0])
        if "Location" in match:
            uk_postcode_pattern =\
                r'\b([A-Z]{1,2}[0-9R][0-9A-Z]? ?[0-9][A-Z]{2}|[A-Z]{1,2}[0-9R][0-9A-Z]?)\b'
            postcodes = re.findall(uk_postcode_pattern, text)
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)
            locations = []
            for ent in doc.ents:
                if ent.label_ in ["GPE", "LOC", "FAC"]:
                    locations.append(ent.text)
            if postcodes!=[]:
                pc = postcodes[0]
            else:
                pc = ""
            try:
                location_output=""
                #limit it to the first 4 matches, anymore could be erroneous/ confuse google
                for i in locations[:3]:
                    location_output+= i + " "
                location_output+= pc
            except IndexError:
                print("No location found")
            return location_output
        #All handles regex
        if self.is_regex(match):
            print("Using regex match")
        else :
            print("Using string match")
        all_matches = [(match.group(), match.start()) for match in re.finditer(match, text)]
        if all_matches:
            successful_match = all_matches[0]
        #For handling nlp if required
        else:
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)
            #see page 21 for entity types
            #https://catalog.ldc.upenn.edu/docs/LDC2013T19/OntoNotes-Release-5.0.pdf
            #ent references entity within the doc
            for ent in doc.ents:
                if match.upper() in ent.label_:
                    return ent.text
            return "No match found"

    def html_parser(self, url : str) -> str :
        """
        This function parses the HTML content of a given URL and returns the text content.
        
        Parameters:
            url (str): The URL of the webpage to be parsed.
        
        Returns:
            str: The text content of the webpage.
        """
        if self.can_fetch(url):
            res = requests.get(url, headers=self.headers, timeout=10)
        else:
            raise PermissionError("Robot.txt disallows access to this link")
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text()

    #Add rate limitting
    @sleep_and_retry
    @limits(calls=2, period=2)
    @daily_limit(max_daily=20)
    def obtain_all_link_info(self, url : str, search_list : list) -> dict:
        """Returns a dictionary of information from the link"""
        output={}
        just_text=self.html_parser(url)
        for i in search_list:
            #Single match search uses NLP and regex
            output[str(i)]=self.single_match_search(just_text, i)
        output['Link']=url

        return output
