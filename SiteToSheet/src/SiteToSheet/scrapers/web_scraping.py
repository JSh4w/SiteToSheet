import re
import spacy
import requests
import time 
from functools import wraps 
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry
from urllib import robotparser
from urllib.parse import urlparse

class WebDataHunter:
        
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"
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

    
    def single_match_search(self, text, match):
        if "(£)" in match:
            successful_match = [(match.group(), match.start()) for match in re.finditer(r'£\d{1,3},\d{1,3}', text)]
            for i in successful_match:
                min_range = i[1]-30
                maxc_range = i[1]+30
                search_text = text[min_range:maxc_range]
                match=str(match).replace("(£)","")
                if match in search_text:
                    return i[0]
                else:
                    return f"No {match} , found this value"+ str(i[0])
        
        if "Location" in match:
            postcode_pattern = r'\b([A-Z]{1,2}[0-9R][0-9A-Z]? ?[0-9][A-Z]{2}|[A-Z]{1,2}[0-9R][0-9A-Z]?)\b'
            postcodes = re.findall(postcode_pattern, text)
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
            location_output= locations[0] + " " + locations[1] + " " + pc

            return location_output
            
        else:
            return("none")
            #if self.is_regex(match):
            #    successful_match = [(match.group(), match.start()) for match in re.finditer(match, text)][0]
            #else :
            #    successful_match = [(match.group(), match.start()) for match in re.finditer(match, text)][0]
            
        #return successful_match

    @sleep_and_retry
    @limits(calls=2, period=2)
    @daily_limit(max_daily=20)
    def obtain_all_link_info(self, url : str, search_list : list) -> dict:
        """Returns a dictionary of information from the link"""
        output={}
        if self.can_fetch(url):
            res = requests.get(url, headers=self.headers)
        else:
            raise Exception("Robot.txt disallows access to this link")
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        just_text=soup.get_text()

        for i in search_list:
            output[str(i)]=self.single_match_search(just_text, i)
        output['Link']=url

        return output 
    
    


