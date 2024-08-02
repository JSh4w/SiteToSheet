import re
import spacy

text="""



3 bedroom flat for rent in Hazellville Road, London, N19








































































































































































































































































































































































































































Skip to content




! It appears that Javascript is disabled on your browser.
            We're sorry, some parts of the Rightmove website don't work at their best without JavaScript enabled.
            Please ensure your JavaScript is turned on to make sure you have the best experience.














open-rightmove-assistant











burger_menu











Buy



Property for sale
New homes for sale




Property valuation
Investors
Mortgages





Rent



Property to rent
Student property to rent





House Prices



Sold house prices
Property valuation




Instant online valuation





Find Agent



Find estate agents





Commercial





                                        Commercial property to rent


Commercial property for sale
Advertise commercial property





Inspire



Moving stories
Property
                                        news
Energy efficiency




Property
                                        guides
Housing trends
Mortgage guides




Overseas blog
Country guides





Overseas



All countries
Spain
France




Portugal
Italy
Greece




Currency
Sell overseas property










                            Sign in




                            My Rightmove




open-rightmove-assistant







































log_in










Sign
                in
My Rightmove


Buy
Property for sale
New
                homes for sale
Property
                valuation
Investors
Mortgages


Rent
Property to rent
Student property to rent


Find Agent
Find estate agents


House prices
Sold house prices
Instant online valuation


Commercial
Commercial property to rent
Commercial property for sale
Advertise


Inspire
Moving
                stories
Property news
Energy
                efficiency
Property
                guides
Housing trends
Overseas blog
Mortgage guides


Overseas
All countries
Spain
France
Portugal
Italy
Greece
Currency
Sell Overseas property



1212Hazellville Road, London, N19£2,200 pcm£508 pwThe amount per month or week you need to pay the landlord.Read more about property rent in our glossary page.Tenancy infoReduced yesterdayLetting detailsLet available date: NowDeposit: £2,538A deposit provides security for a landlord against damage, or unpaid rent by a tenant.Read more about deposit in our glossary page.Min. Tenancy: Ask agentHow long the landlord offers to let the property for.Read more about tenancy length in our glossary page.Let type: Long termFurnish type: FurnishedCouncil Tax: Ask agentPROPERTY TYPE  FlatBEDROOMS  3BATHROOMS  1SIZE  Ask agent1Key featuresCentral heatingDishwasherWashing machineWhite goodsCable/SatelliteBroadband/ADSLDescriptionProperty number 50207. Click the "Request Details" button, submit the form and we'll text & email you within minutes, day or night.Comprising two double and one small single bedroom, kitchen/lounge, bathroom with WC and hallway storage. The block as attractive green spaces in the communal area and is clean and well cared for. Council Tax Band C. Fibre optic broadband available. Parking permit available upon application and payment to Islington Council. If you're interested in this property please click the "request details" button aboveRead full descriptionCOUNCIL TAXA payment made to your local authority in order to pay for local services like schools, libraries, and refuse collection. The amount you pay depends on the value of the property.Read more about council Tax in our glossary page.Ask agentPARKINGDetails of how and where vehicles can be parked, and any associated costs.Read more about parking in our glossary page.YesGARDENA property has access to an outdoor space, which could be private or shared.Ask agentACCESSIBILITYHow a property has been adapted to meet the needs of vulnerable or disabled individuals.Read more about accessibility in our glossary page.Ask agentEnergy Performance CertificateUtilities, rights & restrictionsHazellville Road, London, N19Open mapStreet ViewStationsSchoolsNEAREST STATIONSDistances are straight line measurements from the centre of the postcodeArchway Station0.5 milesCrouch Hill Station0.6 milesUpper Holloway Station0.6 milesBroadband speedAbout the agentVisum, NationwideWeb based Estate Agent Visum is the UK's original online estate and letting agent, helping vendors and landlords since 2004. We offer a full range of lettings and estate agency services across the UK and have directly enabled over 20,000 customers to let or sell their properties away from the constraints of traditional agents.If you are a forward thinking person that wants to avoid paying high agency fees and thinks traditional agents don't give good value for money then you need to speak to us. Our service Read moreMore properties from this agentIndustry affiliationsNotesThese notes are private, only you can see them.Save noteMARKETED BYVisum, NationwideWeb based Estate Agent More properties from this agentCall agentRequest detailsStaying secure when looking for propertyEnsure you're up to date with our latest advice on how to avoid fraud or scams when looking for property online.Visit our security centre to find out more Disclaimer - Property reference 50207. The information displayed about this property comprises a property advertisement. Rightmove.co.uk makes no warranty as to the accuracy or completeness of the advertisement or any linked or associated information, and Rightmove has no control over the content. This property advertisement does not constitute property particulars. The information is provided and maintained by Visum, Nationwide. Please contact the selling agent or developer directly to obtain any information which may be available under the terms of The Energy Performance of Buildings (Certificates and Inspections) (England and Wales) Regulations 2007 or the Home Report if in relation to a residential property in Scotland.
        *This is the average speed from the provider with the fastest broadband package available at this postcode.
        The average speed displayed is based on the download speeds of at least 50% of customers at peak time (8pm to 10pm).
        Fibre/cable services at the postcode are subject to availability and may differ between properties within a postcode.
        Speeds can be affected by a range of technical and environmental factors. The speed at the property may be lower than that
        listed above. You can check the estimated speed and confirm availability to a property prior to purchasing on the
        broadband provider's website. Providers may increase charges. The information is provided and maintained by
        Decision Technologies Limited.

        **This is indicative only and based on a 2-person household with multiple devices and simultaneous usage.
        Broadband performance is affected by multiple factors including number of occupants and devices, simultaneous usage, router range etc.
        For more information speak to your broadband provider.
Map data ©OpenStreetMap contributors.Your search historyYou have no recent searches.Email agentCall agentCall agentEmail agent









                        Download the Rightmove app





























Resources







Stamp Duty Calculator
House Price Index
Property
                                guides
Property news

Buyer
                                guides
Seller
                                guides
Renter
                                guides
Landlord guides
Student
                                guides
Removals

Energy efficiency
Mortgage in Principle
Mortgage Calculator
Mortgage guides





Search







Search homes for sale
Search homes for rent
Commercial for sale
Commercial to rent
Overseas homes for sale
Search sold house prices
Find
                                an agent
Student accommodation
Retirement homes
New
                                homes





Locations







Major towns and cities in the UK
London
Cornwall
Glasgow
Cardiff
Edinburgh
Spain
France
Portugal





Rightmove







Tech
                                blog
About
Press
                                centre
Investor relations
Contact us
Careers
Sign in or create account
HomeViews





Professional








Rightmove
                                Plus

Data
                                Services
Advertise on Rightmove
Overseas agents and developers
Home and property related services
Advertise commercial property
HomeViews Business Hub



"""

nlp = spacy.load("en_core_web_sm")

doc = nlp(text)
locations = []
for ent in doc.ents:
    if ent.label_ in ["GPE", "LOC", "FAC"]:
        locations.append(ent.text)
print(locations)