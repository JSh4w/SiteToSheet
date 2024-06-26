import re
import requests
from bs4 import BeautifulSoup



class WebDataHunter:
        
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",  "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"
        } 

    def link_info(self, link : str):
        """Returns a dictionary of information from the link"""
        output={}
        self.link = link
        res = requests.get(self.link, headers=self.headers)
        output["Link"]=self.link
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        just_text=soup.get_text()
        matches = [(match.group(), match.start()) for match in re.finditer(r'£\d{1,3},\d{3}', just_text)]
        location = [(match.group(), match.start()) for match in re.finditer("for rent in", just_text)]
        location_text=just_text[location[0][1]+11:location[0][1]+120].strip()
        for i in matches:
            index=i[1]
            min_range = index-30
            max_range = index+30
            search_text=just_text[min_range:max_range]
            if "Deposit" in search_text:
                Deposit=i[0]
            else:
                Deposit = "Unknown"
            if "Price" or "pcm" in search_text:
                Price=i[0]
            else:
                Price = "Unknown" 
        output["Deposit"]=Deposit
        output["Price"]=Price
        output["Location"]=location_text

        return output 




