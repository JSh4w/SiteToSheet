#requests deals with extracting information from RightMove
import requests 

#Beautiful soup- https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)#:~:text=Beautiful%20Soup%20is%20a%20Python,is%20useful%20for%20web%20scraping.
# Parses HTML - taking code and extracting relevant information 
from bs4 import BeautifulSoup

#used for rests
import time 
import random

#for converting to csv
import pandas as pd

BOROUGHS ={
    "Islington": "5E93965",
}


max_price = 3500
min_price = 2500
min_bedroom = 3
max_bedroom = 3
radius = 0    # 0 0.25 0.5 1.0 3.0
let_agreed = 'false' # false or true 



def main():  #used to define a function 
    # create lists to store our data
    all_apartment_links = []
    all_description = []
    all_address = []
    all_price = []


    for borough in list(BOROUGHS.values()):
        index =0 
        key= [key for key, value in BOROUGHS.items() if value == borough] ##cycles through keys and values if value = associated borough 
        print(f" Scraping through borough :{key}")
        for pages in range(41): #max number of pages that can go through on rightmove
            # here headers holds a dictionary, User Agent is the key, The value is a string that emulates the user agent of a browser. Very standard 
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }

        if index ==0:
            if radius ==0 :
                rightmove =f'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{borough}&maxBedrooms={max_bedroom}&minBedrooms={min_bedroom}&maxPrice={max_price}&minPrice={min_price}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=partFurnished%2Cfurnished&keywords='
            else:
                rightmove =f'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{borough}&maxBedrooms={max_bedroom}&minBedrooms={min_bedroom}&maxPrice={max_price}&minPrice={min_price}&radius={radius}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=partFurnished%2Cfurnished&keywords='
    
        if index !=0:
            if radius ==0 :
                rightmove =f'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{borough}&maxBedrooms={max_bedroom}&minBedrooms={min_bedroom}&maxPrice={max_price}&minPrice={min_price}&index={index}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=partFurnished%2Cfurnished&keywords='
            else:
                rightmove =f'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{borough}&maxBedrooms={max_bedroom}&minBedrooms={min_bedroom}&maxPrice={max_price}&minPrice={min_price}&radius={radius}&index={index}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=partFurnished%2Cfurnished&keywords='
    
        # request our webpage
        res = requests.get(rightmove, headers=headers)
        # check status
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        # This gets the list of apartments
        apartments = soup.find_all("div", class_="l-searchResult is-list")
        # This gets the number of listings
        number_of_listings = soup.find(
            "span", {"class": "searchHeader-resultCount"}
        )
        number_of_listings = number_of_listings.get_text()
        number_of_listings = int(number_of_listings.replace(",", ""))
        for i in range(len(apartments)):
            # tracks which apartment we are on in the page
            apartment_no = apartments[i]
            print(apartment_no)
            # append link
            apartment_info = apartment_no.find("a", class_="propertyCard-link")
            link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]
            all_apartment_links.append(link)
            # append address
            address = (
                apartment_info.find("address", class_="propertyCard-address")
                .get_text()
                .strip()
            )
            all_address.append(address)
            # append description
            description = (
                apartment_info.find("h2", class_="propertyCard-title")
                .get_text()
                .strip()
            )
            all_description.append(description)
            # append price
            price = (
                apartment_no.find("span", class_="propertyCard-priceValue")
                .get_text()
                .strip()
            )
            all_price.append(price)
        print(f"You have scrapped {pages + 1} pages of apartment listings.")
        print(f"You have {number_of_listings - index} listings left to go")
        print("\n")
        # code to ensure that we do not overwhelm the website
        time.sleep(random.randint(1, 3))
        # Code to count how many listings we have scrapped already.
        index = index + 24
        if index >= number_of_listings:
            break

    # convert data to dataframe
    data = {
        "Links": all_apartment_links,
        "Address": all_address,
        "Description": all_description,
        "Price": all_price,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(r"Right_move/sales_data.csv", encoding="utf-8", header="true", index = False)



if __name__ == "__main__":
    main()

#This code checks if name of file is main. If this is the main python file then it runs.           
