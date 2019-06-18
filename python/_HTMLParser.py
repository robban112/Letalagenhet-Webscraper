from lxml import html
import requests
from bs4 import BeautifulSoup
from enum import Enum
from WebScraper import scrapePages
from SollentunaParser import getAvailableAppartmentsFromSollentuna

class Provider:
    def __init__(self, request_url, appartment_url, location_index, address_index, rooms_index, size_index, 
    floor_index, rent_index, available_until_index, number_of_signed_up, has_duplicates, pathToNextButton="//a[@class='btn next']"):
        self.request_url = request_url
        self.appartment_url = appartment_url
        self.location_index = location_index
        self.address_index = address_index
        self.rooms_index = rooms_index
        self.floor_index = floor_index
        self.size_index = size_index
        self.rent_index = rent_index
        self.available_until_index = available_until_index
        self.number_of_signed_up = number_of_signed_up
        self.has_duplicates = has_duplicates
        self.pathToNextButton = pathToNextButton

FORVALTAREN_URL = 'https://www.forvaltaren.se/ledigt/lagenhet'
HASSELBY_HEM_URL = 'https://bostad.hasselbyhem.se/HSS/Object/object_list.aspx?cmguid=4e6e781e-5257-403e-b09d-7efc8edb0ac8&objectgroup=1'
SOLLENTUNA_HEM_URL = 'https://www.sollentunahem.se/ledigt-just-nu/lagenheter/GetObjects/'
VASBY_HEM_URL = 'https://www.vasbyhem.se/ledigt/sok/lagenhet'
HANINGE_BOSTADER_URL = 'https://minasidor.haningebostader.se/ledigt/sok/lagenhet'
IKANO_BOSTAD_URL = 'https://hyresratt.ikanobostad.se/ledigt/sok/lagenhet'

FORVALTAREN = Provider(FORVALTAREN_URL, 'https://www.forvaltaren.se/ledigt/', 0, 0, 1, 2, 3, 4, 5, 6, False)
HASSELBY_HEM = Provider(HASSELBY_HEM_URL, 'https://bostad.hasselbyhem.se/HSS/Object/', 1, 0, 1, 2, None, 3, 4, 5, False)
SOLLENTUNA_HEM = Provider(SOLLENTUNA_HEM_URL, 'https://www.sollentunahem.se/ledigt/', 0, 1, 1, 2, 3, 4, 5, 6, True)
VASBY_HEM = Provider(VASBY_HEM_URL, 'https://www.vasbyhem.se/ledigt/detalj/', 1, 1, 2, 3, 4, 5, 6, 7, True)
HANINGE_BOSTADER = Provider(HANINGE_BOSTADER_URL, 'https://minasidor.haningebostader.se/ledigt/detalj/', 1, 0, 1, 2, None, 3, 4, 5, False)
IKANO_BOSTAD = Provider(IKANO_BOSTAD_URL, 'https://hyresratt.ikanobostad.se/ledigt/detalj/', 1, 1, 2, 3, 0, 4, 5, None, False)

def getPageContent(provider):
    htmls = scrapePages(provider.request_url, provider.pathToNextButton)
    app_dicts = []
    for html in htmls:
        page_content = BeautifulSoup(html, "html.parser")
        app_dicts.append(getAvailableAppartmentsFrom(provider, page_content))
    return app_dicts

    
def getAvailableAppartmentsFrom(provider, page_content):
    if provider == SOLLENTUNA_HEM:
        return getAvailableAppartmentsFromSollentuna(page_content)
    else:
        return getStandardizedAppartmentsList(page_content, provider)
        

def getStandardizedAppartmentsList(page_content, provider):
    appartments = page_content.find_all("tr")
    app_dict = {}
    for index, appart in enumerate(appartments):
        if index == 0 or (provider.has_duplicates and index % 2 == 0):
            continue
        app_dict[index] = getPropertiesFromProvider(appart, provider, index)
    return app_dict

def getPropertiesFromProvider(appart, provider, index):
    spans = appart.find_all('span')
    a = appart.find_all('a')
    if len(spans) > 0 and len(a) > 0:
        location = spans[provider.location_index].text
        address = a[provider.address_index].text
        rooms = spans[provider.rooms_index].text
        floor = spans[provider.floor_index].text if provider.floor_index != None else 'null'
        size = spans[provider.size_index].text.replace(u'\xa0', '')
        rent = spans[provider.rent_index].text.replace(u'\xa0', '')
        available_until = spans[provider.available_until_index].text
        number_of_people_signed_up = spans[provider.number_of_signed_up].text if provider.number_of_signed_up != None else 'null'
        appartment_url = getLink(a, provider)
        return {
            "location" : location, "address" : address, "rooms" : rooms, 
            "floor" : floor, "size" : size, "rent" : rent, "provider": provider, 
            "appartment_url": appartment_url, "available_until" : available_until, 
            "number_of_people_signed_up" : number_of_people_signed_up
        }
    

def getLink(aelem, provider):
    return provider.appartment_url + aelem[provider.address_index]['href']
    

app = getPageContent(SOLLENTUNA_HEM)
print(app)


