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
     
class WebDataHunter:
    def __init__(self):
        # Option 2: Using multiple lines for each key-value pair
        self.headers = {    
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/71.0.3578.98 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/webp,image/apng,*/*;q=0.8"
        }
    def is_regex(self,pattern):
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
                    raise Exception("Daily limit of 20 requests exceeded")

                func.daily_count += 1
                return func(*args, **kwargs)
            return wrapper
        return decorator
    @staticmethod
    def can_fetch(url):
        rp = robotparser.RobotFileParser()
        parsed_uri = urlparse(url)
        domain = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        rp.set_url(f"{domain}/robots.txt")
        rp.read()
        return rp.can_fetch("*", url)

    #NLP process returns lists of list (text and the corresponding label)
    def nlp_process(self, text, labels) ->list:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        matches=[]
        for ent in doc.ents:
            if ent.label_ in labels:
                matches.append([ent.text, ent.label_])
        return matches


    #Match via regex first then if not found use NLP for more accuracy
    def single_match_search(self, text, match):
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
                else:
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
        if self.can_fetch(url):
            res = requests.get(url, headers=self.headers, timeout=10)
        else:
            raise Exception("Robot.txt disallows access to this link")
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
