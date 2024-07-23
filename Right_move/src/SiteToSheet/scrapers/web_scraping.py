import re
import spacy
import requests
from bs4 import BeautifulSoup



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


        

    def link_info(self, link : str, search_list : list) -> dict:
        """Returns a dictionary of information from the link"""
        output={}
        res = requests.get(link, headers=self.headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        just_text=soup.get_text()

        for i in search_list:
            output[str(i)]=self.single_match_search(just_text, i)
        output['Link']=link

        return output 

